# AWS Deployment Architecture

This document describes the **deployment architecture of the CARMS Data Platform** and how the current local containerized setup can be deployed to AWS using managed cloud services.

The project currently runs locally using **Docker Compose**, and the architecture below shows how the same components can be mapped to AWS infrastructure for production-style deployment.

---

# 1. Overview

The CARMS Data Platform consists of the following main components:

- **PostgreSQL relational database**
- **ETL pipelines** for loading CaRMS program data
- **Embedding generation pipeline** to build a FAISS vector index
- **FastAPI backend** exposing both relational and RAG endpoints
- **Streamlit analytics dashboard**

The platform is designed to run locally using containers and can be deployed to AWS with minimal architectural changes.

---

# 2. Current Local Architecture (Docker Compose)

The project currently runs as a **local containerized data platform** using Docker Compose.

### Containers

| Service | Purpose |
|------|------|
| `db` | PostgreSQL database |
| `init-db` | Creates the relational schema |
| `etl` | Loads CaRMS datasets into PostgreSQL |
| `embeddings` | Generates the FAISS vector index |
| `api` | FastAPI backend exposing database + RAG endpoints |
| `dashboard` | Streamlit analytics dashboard |

### Shared Data Directory

All services share a mounted repository-level directory:

```
data/
├── raw
├── extracted
└── embeddings
```

| Folder | Purpose |
|------|------|
| `raw` | Original CaRMS data files |
| `extracted` | ETL-generated structured files |
| `embeddings` | FAISS vector index |

---

## Local Architecture Diagram

```
                    ┌─────────────────────────────┐
                    │      Docker Compose         │
                    └──────────────┬──────────────┘
                                   │
     ┌─────────────────────────────┼─────────────────────────────┐
     │                             │                             │
     ▼                             ▼                             ▼
┌──────────────┐           ┌──────────────┐              ┌──────────────┐
│   init-db    │           │     etl      │              │  embeddings  │
│ create schema│           │ load data    │              │ build FAISS  │
└──────┬───────┘           └──────┬───────┘              └──────┬───────┘
       │                          │                             │
       └──────────────┬───────────┴──────────────┬──────────────┘
                      │                          │
                      ▼                          ▼
               ┌──────────────┐         ┌────────────────┐
               │ PostgreSQL   │         │ data/          │
               │ normalized DB│         │ raw/extracted/ │
               └──────┬───────┘         │ embeddings/    │
                      │                 └────────────────┘
                      ▼
               ┌──────────────┐
               │   FastAPI    │
               │ DB + RAG API │
               └──────┬───────┘
                      ▼
               ┌──────────────┐
               │  Streamlit   │
               │ Dashboard    │
               └──────────────┘
```

---

# 3. Target AWS Deployment Architecture

The target AWS architecture keeps the same logical components while replacing local infrastructure with managed AWS services.

### AWS Services

| Component | AWS Service | Purpose |
|-----------|-------------|--------|
| Database | Amazon RDS PostgreSQL | Managed relational database |
| API + RAG | ECS Fargate or AWS App Runner | Run the FastAPI container |
| Data storage | Amazon S3 | Store raw data and FAISS artifacts |
| Secrets | AWS Secrets Manager | Store API keys and database credentials |
| ETL orchestration | ECS scheduled tasks / Dagster / Step Functions | Run ETL and embedding generation |
| Dashboard | App Runner / ECS / local | Streamlit analytics interface |

---

## AWS Architecture Diagram

```
                    ┌─────────────────────────────────────────────────────┐
                    │                     AWS Cloud                       │
                    │                                                     │
Users / Clients ───▶│   ┌──────────────────────────────┐                  │
                    │   │   ECS Fargate / App Runner   │                  │
                    │   │      FastAPI + RAG API       │                  │
                    │   └───────────────┬──────────────┘                  │
                    │                   │                                 │
                    │                   ▼                                 │
                    │         ┌────────────────────┐                      │
                    │         │   Amazon RDS       │                      │
                    │         │   PostgreSQL       │                      │
                    │         └────────────────────┘                      │
                    │                                                     │
                    │                   ▲                                 │
                    │                   │                                 │
                    │   ┌───────────────┴──────────────┐                  │
                    │   │ ETL / Embeddings Jobs        │                  │
                    │   │ ECS Tasks / Dagster /        │                  │
                    │   │ Step Functions               │                  │
                    │   └───────────────┬──────────────┘                  │
                    │                   │                                 │
                    │                   ▼                                 │
                    │         ┌────────────────────┐                      │
                    │         │     Amazon S3      │                      │
                    │         │ raw + extracted +  │                      │
                    │         │ embeddings / FAISS │                      │
                    │         └────────────────────┘                      │
                    │                                                     │
                    │         ┌────────────────────┐                      │
                    │         │ Secrets Manager    │                      │
                    │         │ API keys / DB creds│                      │
                    │         └────────────────────┘                      │
                    └─────────────────────────────────────────────────────┘
```

---

# 4. Storage Strategy

### Relational Database

The normalized relational schema is stored in **Amazon RDS PostgreSQL**.

### Raw and Processed Data

Source files and ETL outputs are stored in **Amazon S3**, including:

- raw Excel and ZIP files
- extracted CSV files
- generated metadata artifacts

### FAISS Vector Index

The FAISS index can be handled in several ways:

1. Bundled inside the API container image
2. Stored in S3 and downloaded at container startup
3. Stored in Amazon EFS and mounted into the container

For lightweight deployments, storing the FAISS index in **S3** is usually sufficient.

---

# 5. Deployment Flow

### Step 1 — Create RDS Database

Provision an **Amazon RDS PostgreSQL** instance and configure:

- database name
- credentials
- VPC and security groups

Run schema initialization:

```
python -m src.db.init_db
```

with `DATABASE_URL` pointing to the RDS instance.

---

### Step 2 — Build and Push Docker Image

Build the API container image from the project Dockerfile and push it to **Amazon ECR**.

Example:

```
docker build -t carms-api .
docker tag carms-api:latest <aws_account>.dkr.ecr.<region>.amazonaws.com/carms-api
docker push <aws_account>.dkr.ecr.<region>.amazonaws.com/carms-api
```

---

### Step 3 — Run ETL and Embedding Pipelines

Execute ETL and embedding generation using:

- ECS tasks
- scheduled ECS jobs
- Dagster running on ECS
- Step Functions workflows

Generated data and vector artifacts are stored in **S3**.

---

### Step 4 — Deploy FastAPI API

Deploy the API container using:

- **AWS App Runner** for simple managed deployments  
or
- **ECS Fargate** for more infrastructure control.

Environment variables are injected from **Secrets Manager**.

---

### Step 5 — Deploy or Connect the Dashboard

The Streamlit dashboard can:

- run locally against the deployed API
- or be deployed as a container on App Runner or ECS.

---

# 6. Environment Variables

The AWS deployment uses the same configuration model as the local environment.

| Variable | Purpose |
|------|------|
| `DATABASE_URL` | PostgreSQL connection string |
| `DATA_DIR` | Base data directory |
| `FAISS_PATH` | Path to FAISS vector index |
| `OPENAI_API_KEY` | OpenAI API key |
| `API_URL` | Base URL for the Streamlit dashboard |

Example:

```
DATABASE_URL=postgresql+psycopg2://user:password@rds-endpoint:5432/carms_db
DATA_DIR=/data
FAISS_PATH=/data/embeddings/faiss_index
OPENAI_API_KEY=...
```

---

# 7. Security Considerations

- Place **RDS in private subnets**
- Use **security groups** to restrict database access
- Store secrets in **AWS Secrets Manager**
- Use **IAM roles for ECS tasks**
- Avoid storing credentials in the container image

---

# 8. Cost Optimization

For a demonstration deployment:

- use small **RDS instance types**
- start with **single-AZ** deployment
- run ETL pipelines as **on-demand tasks**
- keep dashboard optional if API access is sufficient

---

# 9. Summary

The CARMS Data Platform implements a reproducible **local containerized data platform** with:

- normalized relational storage
- ETL data ingestion pipelines
- FAISS vector indexing
- FastAPI API layer
- Streamlit analytics dashboard

The AWS architecture preserves this design while replacing local infrastructure with **managed cloud services such as RDS, ECS, S3, and Secrets Manager**, enabling scalable deployment with minimal changes to the application code.