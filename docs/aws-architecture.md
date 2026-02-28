# AWS Deployment Architecture (Target)

This document describes a **target architecture** for running the CARMS Data Platform on AWS using a containerized approach. It is intended as a blueprint for production-style deployment and can be implemented incrementally.

## Overview

- **PostgreSQL** → Amazon RDS (or Aurora PostgreSQL)
- **Application (FastAPI + RAG)** → Container on ECS Fargate or AWS App Runner
- **Raw data / FAISS index** → Amazon S3 (with optional sync to container or EFS)
- **Orchestration (Dagster)** → Optional: ECS task, Lambda-triggered, or EC2
- **Dashboard (Streamlit)** → Optional: App Runner or ECS, or run locally against deployed API

## Suggested Diagram (Logical)

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                      AWS Cloud                           │
                    │  ┌─────────────┐    ┌──────────────┐    ┌────────────┐  │
  Users / API       │  │   ALB or     │───▶│  ECS Fargate  │    │    RDS     │  │
  clients           │  │ App Runner  │    │  (FastAPI +   │───▶│ PostgreSQL │  │
  ────────────────▶ │  │  (API)      │    │   RAG/FAISS)  │    │            │  │
                    │  └─────────────┘    └──────┬───────┘    └────────────┘  │
                    │                            │                             │
                    │                            │ read at build/time          │
                    │                            ▼                             │
                    │  ┌─────────────┐    ┌──────────────┐                     │
                    │  │     S3      │◀───│  ETL /       │                     │
                    │  │ Raw data +  │    │  Dagster     │                     │
                    │  │ FAISS index │    │              │                     │
                    │  └─────────────┘    └──────────────┘                     │
                    └─────────────────────────────────────────────────────────┘
```

## Components

| Component | AWS Service | Notes |
|-----------|-------------|--------|
| **Database** | RDS PostgreSQL or Aurora | Same schema and connection string; use security groups to allow only API. |
| **API + RAG** | ECS Fargate or App Runner | Build image from project Dockerfile; set `DATABASE_URL`, `FAISS_PATH`, and optionally mount S3/EFS for FAISS index. |
| **Data & embeddings** | S3 | Store raw ZIP/Excel/CSV and pre-built FAISS index; copy into container at build or mount via EFS/volume. |
| **Secrets** | Secrets Manager | Store `OPENAI_API_KEY`, DB credentials; inject into ECS task or App Runner. |
| **Orchestration** | ECS (Dagster) or Step Functions | Run ETL and embedding build on schedule or on event; write FAISS to S3 and trigger API image rebuild if needed. |

## Deployment Steps (High Level)

1. **Create RDS**  
   - PostgreSQL 16; configure security group and VPC.  
   - Run schema init (e.g. `python -m src.db.init_db` with RDS endpoint as `DATABASE_URL`).

2. **Build and push API image**  
   - Use existing `Dockerfile` in `carms-data-platform-demo/`.  
   - Push to Amazon ECR:  
     `aws ecr get-login-password --region <region> | docker login ...`  
     `docker build -t carms-api . && docker tag ... && docker push ...`

3. **Run ETL and embeddings**  
   - Run once (locally or in a one-off ECS task) with `DATABASE_URL` pointing to RDS.  
   - Upload FAISS index (and optional raw data) to S3.

4. **Deploy API**  
   - **App Runner**: Create service from ECR image; set env vars (`DATABASE_URL`, `FAISS_PATH`, `OPENAI_API_KEY` from Secrets Manager). If FAISS is in image, set `FAISS_PATH` to path inside image; otherwise use EFS or init container that pulls from S3.  
   - **ECS Fargate**: Task definition with same env; optionally mount EFS volume for `/data` and sync FAISS from S3 at startup.

5. **Dashboard**  
   - Set `API_URL` to the deployed API URL; run Streamlit locally or deploy a second container (e.g. App Runner) that points to the API.

## Environment Variables for AWS

- `DATABASE_URL` — RDS connection string (e.g. `postgresql+psycopg2://user:pass@rds-endpoint:5432/carms_db`).  
- `FAISS_PATH` — Path to FAISS index inside container (e.g. `/data/embeddings/faiss_index`) or where EFS is mounted.  
- `DATA_DIR` — Base path for data/embeddings if using volume mount.  
- `OPENAI_API_KEY` — From Secrets Manager or task environment (secure).

## Security and Cost Notes

- Prefer private subnets for RDS and ECS; put ALB/App Runner in public subnets.  
- Use IAM roles for ECS tasks (no long-lived keys).  
- Start with minimal instance sizes and single-AZ for cost control; scale as needed.

