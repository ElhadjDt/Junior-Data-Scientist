# Junior Data Scientist
Public-facing CaRMS data scraped from the CaRMS website.

We are modernizing our infrastructure using PostgreSQL, SQLAlchemy/SQLModel, Dagster, LangChain, and FastAPI. Use the data in this repository to show us your data engineering, data science, and/or visualization skills. Use our stack to show us what you can do! Build something, provide your project GitHub repository link in your application to the Junior Data Scientist position in our group, get an interview, and present your work to us.

A sample project using our stack with a containerized approach, particularly on AWS will get our attention. 

# 1. Relational Database Design, Normalization & Population

## 1.1 Overview

This project begins by transforming raw CaRMS program data into a fully normalized relational PostgreSQL database.  
Two Excel files serve as the foundation for the schema design and population:

- **1503_discipline.xlsx**  
- **1503_program_master.xlsx**

The discipline file contains simple key–value pairs, while the program master file contains multiple attributes that must be decomposed to avoid update, insertion, and deletion anomalies.  
> “Creating a single table program with that file will not be normalized… thus we will need to break down the file into 4 tables for normalization purpose.”  
> 

The final schema follows **3rd Normal Form (3NF)** and ensures long‑term maintainability, consistency, and clean referential integrity.

---

## 1.2 Source Files

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

---

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

---

## 1.3 Normalized Schema (3NF)

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
| discipline_id       | FK → discipline |
| school_id           | FK → school |
| site_id             | FK → site |
| stream_id           | FK → stream |
| program_stream_id   | PK   |
| program_name        | Text |
| program_stream_name | Text |
| program_url         | Text (url)|
---

## 1.4 ETL & Database Population

The ETL pipeline loads the Excel files **row by row**, and inserts them into the PostgreSQL database.

Tools used:
- **SQLModel** for ORM models  
- **Docker Compose** for PostgreSQL container  
- **Manual ETL or Dagster UI** for orchestration  

> “ docker‑compose + SQLModel + ETL (manual)/Dagster UI ”  
> 

These two files are sufficient to build the **core relational PostgreSQL database** storing and maintaining all disciplines and programs.

---

# 2. QA RAG System (Retrieval-Augmented Generation)

## 2.1 Overview

In addition to the relational database, the project includes a **Retrieval‑Augmented Generation (RAG)** pipeline designed to answer questions about CaRMS programs using program descriptions.

The raw program descriptions are provided in 6 ZIP archives containing Markdowns (`.md`), JSONs, and a CSV file.  
I only use the CSV format file version of the programs description:

- `1503_program_description_x_section.csv`

Then created a table in the relational database named `program_document` to store the description.



## 2.2 Program Document Table

The CSV file is transformed into a structured table that links each description to its corresponding program stream.

**Table: program_document** (main columns)

| Column               | Type | Notes |
|----------------------|------|-------|
| id                   | PK   | Auto-increment |
| program_stream_id    | FK   | Links to normalized program table |
| section_name         | Text | Section of the description |
| content              | Text | Raw text content |
| source               | Text | URL or metadata |

This table becomes the **single source of truth** for all downstream retrieval and QA operations.

## 2.3 Text Chunking & Embeddings

Long program descriptions are split into smaller, semantically meaningful chunks.  
Each chunk is then embedded using an OpenAI embedding model.

Pipeline:

1. **Chunking**  
   - Split long text into smaller segments  
   - Preserve section metadata  

2. **Embedding**  
   - Convert each chunk into a dense vector  
   - Store vectors in a FAISS index  



## 2.4 FAISS Vector Store

The embeddings are stored in a **FAISS vector index**, enabling fast similarity search.

- Efficient retrieval of top‑5 relevant chunks  
- Reproducible index build  
- Integrated with LangChain retrievers  


![FAISS vector store creation](docs/imgs/faiss.png)


## 2.5 Retrieval-Augmented Generation Pipeline

The RAG pipeline follows a standard architecture:

1. **User question**  
2. **Retriever**  
   - FAISS returns the top 5 most relevant chunks  
3. **LLM reasoning**  
   - model (`gpt-4o-mini`)  
4. **Answer generation**   



This ensures that all answers are grounded in real CaRMS program descriptions.

---
# 3. FastAPI Backend (Database + QA Endpoints)

## 3.1 Overview

FastAPI serves as the backend layer of the platform, exposing both the **relational database** and the **RAG QA system** through REST endpoints.  
This allows external applications, dashboards, or analysts to interact with the relational Postgres database and the QA engine.

The backend is fully modular and integrates:

- SQLModel / SQLAlchemy ORM models  
- Postgre db 
- FAISS + LangChain RAG pipeline  
- Automatic API documentation via `/docs`  

---

## 3.2 Architecture

The FastAPI backend is organized into two main modules:

### **1. Database Endpoints**
These endpoints expose normalized relational data:

![data base api](docs/imgs/db_api.png)

All responses are returned as JSON objects.



---

### **2. QA Endpoints (RAG System)**
These endpoints allow users to query the RAG pipeline:


![QA API](docs/imgs/qa_api.png)

This makes the QA system accessible as a simple HTTP API.

---

## 3.3 Relational Database Endpoints (with execution screenshots)

Below are all relational endpoints exposed by the FastAPI backend, each with a placeholder for execution screenshots stored in `docs/imgs/`.

---

###  Disciplines

#### **GET /disciplines/**
List all disciplines.  
![List Disciplines](docs/imgs/disciplines_list.png)

#### **GET /disciplines/{discipline_id}**
Retrieve a specific discipline.  
![Get Discipline](docs/imgs/discipline_detail.png)

#### **GET /disciplines/{discipline_id}/programs**
List all programs for a discipline.  
![Programs by Discipline](docs/imgs/programs_by_discipline.png)

---

###  Programs

#### **GET /programs/**
List all programs.  
![List Programs](docs/imgs/programs_list.png)

#### **GET /programs/{program_stream_id}**
Retrieve a program by stream ID.  
![Program by Stream](docs/imgs/program_by_stream.png)

---

###  Schools

#### **GET /schools/**
List all schools.  
![List Schools](docs/imgs/schools_list.png)

#### **GET /schools/{school_id}**
Retrieve a specific school.  
![Get School](docs/imgs/school_detail.png)

#### **GET /schools/{school_id}/programs**
List all programs offered by a school.  
![School Programs](docs/imgs/school_programs.png)

---

###  Sites

#### **GET /sites/**
List all sites.  
![List Sites](docs/imgs/sites_list.png)

#### **GET /sites/{site_id}**
Retrieve a specific site.  
![Get Site](docs/imgs/site_id.png)

#### **GET /sites/{site_id}/programs**
List all programs associated with a site.  
![Site Programs](docs/imgs/site_programs.png)

---

###  Streams

#### **GET /streams/**
List all program streams.  
![List Streams](docs/imgs/streams_list.png)

---

# 4. Installation & Setup

This section will be completed later.  
It will include instructions for:

- Cloning the repository  
- Setting up the PostgreSQL database (Docker Compose)  
- Installing Python dependencies  
- Running the ETL pipeline  
- Starting the FastAPI backend  
- Running Dagster for orchestration  
