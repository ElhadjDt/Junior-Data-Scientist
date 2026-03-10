# CARMS Data Platform — End-to-End Data Engineering Project

This project implements a **data platform built around public CaRMS residency program data**.  
It demonstrates how raw datasets can be transformed into a structured analytical platform with automated pipelines, a relational database, an API layer, and a Retrieval-Augmented Generation (RAG) system.

The platform includes:

- **Automated ETL pipelines** for transforming CaRMS datasets
- A **normalized PostgreSQL relational database (3NF)**
- A **FastAPI backend** exposing relational and QA endpoints
- A **Streamlit analytics dashboard** for data exploration
- A **RAG pipeline** using LangChain, OpenAI embeddings, and FAISS
- **Containerized infrastructure** using Docker and Docker Compose
- **Optional Dagster orchestration** for ETL workflow visualization
- A **production-oriented AWS architecture design**

The goal is to demonstrate practical workflows in data engineering and data science within a reproducible containerized environment.

---

## Technology Stack

- **PostgreSQL** — relational data storage  
- **SQLModel / SQLAlchemy** — database ORM and schema modeling  
- **Dagster** — optional ETL orchestration  
- **LangChain + OpenAI** — RAG QA system  
- **FAISS** — vector similarity search  
- **FastAPI** — REST API backend  
- **Streamlit** — analytics dashboard  
- **Docker & Docker Compose** — containerized infrastructure  

A target **AWS deployment architecture** is also provided in:
[AWS Deployment Architecture](docs/aws-architecture.md)

---

## Table of Contents
1. [System Architecture](#1-system-architecture)
2. [Installation & Setup](#2-installation--setup)  
3. [Relational Database Design](#3-relational-database-design-normalization--population)  
4. [RAG QA System](#4-qa-rag-system-retrieval-augmented-generation)  
5. [FastAPI Backend](#5-fastapi-backend-database--qa-endpoints)
   
---

## 1. System Architecture

The platform is composed of four main layers:

1. **Data Layer**
   - Raw CaRMS datasets (Excel, CSV, ZIP)
   - PostgreSQL relational database

2. **Processing Layer**
   - ETL pipelines for data ingestion
   - Embedding generation pipeline

3. **Application Layer**
   - FastAPI backend
   - RAG QA system

4. **Presentation Layer**
   - Streamlit analytics dashboard
     
---

# 2. Installation & Setup

This section describes how to build and run the **CARMS Data Platform using Docker Compose**.  
The platform includes PostgreSQL, ETL pipelines, FAISS embeddings generation, a FastAPI backend, a Streamlit analytics dashboard, and optional Dagster orchestration.

All components run in **containerized services**, enabling reproducible local execution and a deployment pattern compatible with AWS container services.


# 2.1 Prerequisites

Ensure the following tools are installed:

- Docker
- Docker Compose
- Git

Verify installation:

```bash
docker --version
docker compose version
```

# 2.2 Clone the Repository

```bash
git clone https://github.com/ElhadjDt/Junior-Data-Scientist.git
cd Junior-Data-Scientist/carms-data-platform-demo
```

# 2.3 Configure Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

# 2.4 Data Directory Structure

The repository expects a **data directory located at the repository root**.

Project layout:

```
repo/
├── carms-data-platform-demo/
├── data/
│   └── raw/
└── docs/
```

Initially, the `data` directory should contain only the **raw CaRMS datasets**:

```
data/
└── raw
    ├── 1503_discipline.xlsx
    ├── 1503_program_master.xlsx
    ├── 1503_program_descriptions_x_section.zip
    └── other CaRMS archives
```

During execution, the pipeline automatically generates additional directories:

```
data/
├── raw
├── extracted
└── embeddings
```

| Directory | Purpose |
|----------|--------|
| raw | Original CaRMS data files |
| extracted | Processed CSV files extracted from archives |
| embeddings | FAISS vector index used by the RAG system |

# 2.5 Build the Platform Image

Build the Docker image containing the application environment.

```bash
docker compose build
```

This image contains:

- Python runtime
- project dependencies
- ETL pipelines
- FastAPI backend
- Streamlit dashboard
- Dagster orchestration dependencies

# 2.6 Start PostgreSQL

Start the PostgreSQL database container:

```bash
docker compose up -d db
```

Verify that the service is running:

```bash
docker compose ps
```

# 2.7 Initialize the Database Schema

Create all relational database tables:

```bash
docker compose run --rm init-db
```

This step builds the normalized PostgreSQL schema defined with SQLModel.

# 2.8 Run the ETL Pipeline

Load CaRMS datasets into the database:

```bash
docker compose run --rm etl
```

The ETL process performs the following steps:

1. Extract ZIP archives  
2. Load discipline data  
3. Load program data  
4. Load program descriptions  

# 2.9 Generate Embeddings and Build the FAISS Index

Create embeddings used by the RAG QA system:

```bash
docker compose run --rm embeddings
```

This step:

- splits program descriptions into chunks
- generates OpenAI embeddings
- builds the FAISS similarity index

The vector store is stored in:

```
data/embeddings/faiss_index
```

# 2.10 Start the API and Analytics Dashboard

Launch the backend API and visualization dashboard:

```bash
docker compose up -d api dashboard
```

Services will be available at:

| Service | URL |
|--------|-----|
| FastAPI documentation | http://localhost:8000/docs |
| Streamlit dashboard | http://localhost:8501 |

Example Streamlit dashboard interface:
![List Streams](docs/imgs/dashboard.png)

# 2.11 Optional: Start Dagster Orchestration UI

The platform also includes **Dagster** as an optional orchestration layer for visualizing and executing ETL workflows.

Start Dagster:

```bash
docker compose up -d dagster
```

Dagster will be available at:

```
http://localhost:3000
```

The Dagster interface allows:

- visualizing ETL pipelines
- manually launching pipeline runs
- inspecting pipeline logs
- monitoring workflow execution

Dagster interacts with the same PostgreSQL database and shared data directory used by the other services.

Stop Dagster:

```bash
docker compose stop dagster
```
Example Dagster orchestration interface:

![Dagster Pipeline](docs/imgs/dagster_pipeline.png)


# 2.12 Monitoring Services

Check running containers:

```bash
docker compose ps
```

View logs for the API:

```bash
docker compose logs -f api
```

View logs for the dashboard:

```bash
docker compose logs -f dashboard
```

# 2.13 Stop the Platform

Stop all running services:

```bash
docker compose down
```

To stop services and remove the PostgreSQL volume:

```bash
docker compose down -v
```


# 2.14 Complete Setup Workflow

Full setup sequence:

```bash
docker compose build
docker compose up -d db
docker compose run --rm init-db
docker compose run --rm etl
docker compose run --rm embeddings
docker compose up -d api dashboard
```

(Optional Dagster)

```bash
docker compose up -d dagster
```

After these steps, the entire **CARMS Data Platform** will be operational.


## 2.15 AWS Deployment (Target Architecture)

A production-style **containerized deployment on AWS** is described in  
[AWS Deployment Architecture](docs/aws-architecture.md).

The architecture outlines how the platform can be deployed using managed AWS services:

- **Amazon RDS (PostgreSQL)** for the relational database  
- **ECS Fargate** or **AWS App Runner** for the FastAPI + RAG API  
- **Amazon S3** for raw datasets and the FAISS vector index  
- **AWS Secrets Manager** for secure storage of `OPENAI_API_KEY` and database credentials  
- **Dagster (ECS task)** or **AWS Step Functions** for scheduled ETL and embedding generation  

This architecture enables a fully containerized data platform with scalable API services, managed database infrastructure, and cloud storage for vector search artifacts.

---

# 3. Relational Database Design, Normalization & Population

## 3.1 Overview

This project begins by transforming raw CaRMS program data into a fully normalized relational PostgreSQL database.
Two Excel files serve as the foundation for the schema design and population:

- **1503_discipline.xlsx**
- **1503_program_master.xlsx**

The discipline file contains simple key–value pairs, while the program master file contains multiple attributes that must be decomposed to avoid update, insertion, and deletion anomalies.
> “Creating a single table program with that file will not be normalized… thus we will need to break down the file into 4 tables for normalization purpose.”
>

The final schema follows **3rd Normal Form (3NF)** and ensures long‑term maintainability, consistency, and clean referential integrity.



## 3.2 Source Files

### **1. 1503_discipline.xlsx**
Contains:
- `discipline_id`
- `discipline_name`

This file maps directly to a normalized table:

**Table: discipline**
| Column          | Type |
|-----------------|------|
| discipline_id   | PK   |
| discipline_name | Text |

> “A table discipline is thus created.”
>



### **2. 1503_program_master.xlsx**
This file contains multiple attributes mixed together:

- discipline
- school
- program
- program stream
- site
- program URL

Storing this in a single table would violate normalization rules.
Therefore, the file is decomposed into **four relational tables**.



## 3.3 Normalized Schema (3NF)

### **Table: school**
| Column      | Type |
|-------------|------|
| school_id   | PK   |
| school_name | Text |
---
### **Table: site**
| Column    | Type |
|-----------|------|
| site_id   | PK (auto‑increment) |
| site_name | Text |
---
### **Table: stream**
| Column    | Type |
|-----------|------|
| stream_id | PK (auto‑increment) |
| stream    | Text |
---
### **Table: program**
| Column              | Type |
|---------------------|------|
| program_stream_id   | PK   |
| discipline_id       | FK → discipline |
| school_id           | FK → school |
| site_id             | FK → site |
| stream_id           | FK → stream |
| program_name        | Text |
| program_stream_name | Text |
| program_url         | Text (url)|
---

## 3.4 ETL & Database Population

The ETL pipeline loads the Excel files **row by row**, and inserts them into the PostgreSQL database.

Tools used:
- **SQLModel** for ORM models
- **Docker Compose** for PostgreSQL container
- **Manual ETL or Dagster UI** for orchestration

> “ docker‑compose + SQLModel + ETL (manual)/Dagster UI ”
>

These two files are sufficient to build the **core relational PostgreSQL database** storing and maintaining all disciplines and programs.

---

# 4. QA RAG System (Retrieval-Augmented Generation)

## 4.1 Overview

In addition to the relational database, the project includes a **Retrieval‑Augmented Generation (RAG)** pipeline designed to answer questions about CaRMS programs using program descriptions.

The raw program descriptions are provided in 6 ZIP archives containing Markdowns (`.md`), JSONs, and a CSV file.
I only use the CSV format file version of the programs description:

- `1503_program_description_x_section.csv`

Then created a table in the relational database named `program_document` to store the description.



## 4.2 Program Document Table

The CSV file is transformed into a structured table that links each description to its corresponding program stream.

**Table: program_document** (main columns)

| Column               | Type | Notes |
|----------------------|------|-------|
| id                   | PK   | Auto-increment |
| program_stream_id    | FK   | Links to normalized program table |
| section_name         | Text | Section of the description |
| content              | Text | Raw text content |
| source               | Text | URL |

This table becomes the **single source of truth** for all downstream retrieval and QA operations.

Thus, below is the complete normalized relational schema created:

![POSTGRES RDB NORMALIZE RELATIONS](docs/imgs/db_relations.png)

## 4.3 Text Chunking & Embeddings

Long program descriptions are split into smaller, semantically meaningful chunks.
Each chunk is then embedded using an OpenAI embedding model.

Pipeline:

1. **Chunking**
   - Split long text into smaller segments
   - Preserve section metadata

2. **Embedding**
   - Convert each chunk into a dense vector
   - Store vectors in a FAISS index



## 4.4 FAISS Vector Store

The embeddings are stored in a **FAISS vector index**, enabling fast similarity search.

- Efficient retrieval of top‑5 relevant chunks
- Reproducible index build
- Integrated with LangChain retrievers


![FAISS vector store creation](docs/imgs/faiss.png)


## 4.5 Retrieval-Augmented Generation Pipeline

The RAG pipeline follows a standard architecture:

1. **User question**
2. **Retriever**
   - FAISS returns the top 5 most relevant chunks
3. **LLM reasoning**
   - model (`gpt-4o-mini`)
4. **Answer generation**



This ensures that all answers are grounded in real CaRMS program descriptions.

---

# 5. FastAPI Backend (Database + QA Endpoints)

## 5.1 Overview

The API layer acts as the main interface between the data platform and external applications.

The backend is fully modular and integrates:

- SQLModel / SQLAlchemy ORM models
- Postgre db
- FAISS + LangChain RAG pipeline
- Automatic API documentation via `/docs`



## 5.2 Architecture

The FastAPI backend is organized into two main modules:

### **1. Database Endpoints**
These endpoints expose normalized relational data:

![data base api](docs/imgs/db_api.png)



### **2. QA Endpoints (RAG System)**
These endpoints allow users to query the RAG pipeline:


![QA example_execution](docs/imgs/qa_api.png)
![QA example2_execution](docs/imgs/qa_qr.png)
This makes the QA system accessible as a simple HTTP API.


## 5.3 Relational Database Endpoints

Detailed endpoint execution examples and screenshots are available in:

[API Endpoints Documentation](docs/api-endpoints.md)
