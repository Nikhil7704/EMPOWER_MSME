# EmpowerMSME — High-Performance Python FastAPI Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![LangChain](https://img.shields.io/badge/LangChain-Python-1C3C3C?logo=chainlink&logoColor=white)](https://python.langchain.com)

A production-grade, asynchronous REST API microservice and AI engine powering the **EmpowerMSME** digital financial ecosystem. Built with a decoupled client-server architecture serving both the Next.js React frontend and AI agent pipelines.

---

## Architecture Overview

```text
               ┌────────────────────────────────────────────────────────┐
               │              Next.js 16 (React 19) Frontend            │
               │              Port 3000 (UI / State / SSR)              │
               └───────────────────────────┬────────────────────────────┘
                                           │
                         HTTP REST + JWT Bearer Tokens
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │              Python FastAPI Backend (Port 8000)         │
               ├───────────────────────────┬────────────────────────────┤
               │  Interactive Swagger UI   │  Pydantic v2 Validators    │
               │  OAuth2 / JWT RBAC Auth   │  7-Factor Credit Engine    │
               │  SQLAlchemy 2.0 ORM       │  LangChain + Gemini RAG    │
               └───────────────────────────┴────────────────────────────┘
                                           │
                         SQLite / PostgreSQL Database Engine
```

---

## Key Features

1. **Enterprise Role-Based Access Control (RBAC):**
   - JWT sessions with bcrypt salt hashing.
   - Guarded dependency endpoints for `BUSINESS`, `INVESTOR`, and `ADMIN` personas.

2. **7-Factor Transparent Credit Scoring Engine:**
   - Interpretable weighted linear model scoring alternative financial indicators (GST filing consistency, cash flow variance, debt-to-income, revenue scale).
   - Maps scores (300–900) to Prime, Standard, and Subprime risk tiers with actionable factor contribution breakdowns.

3. **LangChain & Google Gemini RAG Knowledge Engine:**
   - Semantic retrieval over Indian financial inclusion schemes (MUDRA, PMEGP, SIDBI, GST Composition).
   - Dynamic AI pitch generation (Professional, Emotional, and Data-Driven variants).

4. **Fintech Transaction Ledger & P2P Circles:**
   - Loan origination, amortization schedules, and EMI payment tracking.
   - P2P Community Lending Circles (ROSCAs) with member trust scores.
   - Immutable security and financial audit logging.

5. **Auto-Generated OpenAPI & Swagger Documentation:**
   - Full live testing sandbox at `http://127.0.0.1:8000/docs`.

---

## Directory Structure

```text
backend/
├── app/
│   ├── api/                  # FastAPI Route Controllers
│   │   ├── auth.py           # Login, Register, JWT, /me
│   │   ├── loans.py          # Loan origination & status timeline
│   │   ├── campaigns.py      # MSME campaigns & investment ledger
│   │   ├── repayments.py     # Amortization & EMI processing
│   │   ├── credit.py         # 7-factor credit scoring engine
│   │   ├── lending_circles.py# P2P mutual credit groups
│   │   ├── analytics.py      # Business & investor portfolio metrics
│   │   ├── business.py       # MSME profile & KYC metadata
│   │   ├── user.py           # Investor portfolio returns
│   │   ├── admin.py          # KYC verification & audit logs
│   │   ├── chat.py           # LangChain RAG & Story Builder
│   │   └── deps.py           # DB session & RBAC dependency injection
│   ├── core/
│   │   ├── config.py         # Settings & environment variables
│   │   ├── database.py       # SQLAlchemy engine & session factory
│   │   └── security.py       # Bcrypt hashing & JWT utilities
│   ├── models/
│   │   └── models.py         # 8 Relational Database Models
│   ├── schemas/
│   │   └── schemas.py        # Pydantic v2 Request/Response Models
│   ├── services/
│   │   ├── credit_service.py # Credit scoring algorithm
│   │   ├── rag_service.py    # Semantic search & Gemini LLM
│   │   └── audit_service.py  # System event logging
│   └── main.py               # FastAPI App & Middleware Assembly
├── seed.py                   # Demo database seeder
├── test_api.py               # 12 Automated integration test suites
├── run.py                    # Uvicorn launcher
└── requirements.txt          # Python dependencies
```

---

## Quickstart Guide

### 1. Set Up Virtual Environment

```bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed Database with Demo Accounts

```bash
python seed.py
```

**Pre-configured demo accounts:**
* **Business:** `business@demo.com` / `demo1234`
* **Investor:** `investor@demo.com` / `demo1234`
* **Admin:** `admin@demo.com` / `demo1234`

### 4. Run Automated Integration Tests

```bash
python test_api.py
```
*(Runs 12 comprehensive end-to-end tests validating Auth, Loans, Investments, Repayments, Credit Engine, Analytics, and RAG pipelines.)*

### 5. Launch the Server

```bash
python run.py
```

* API Server: `http://127.0.0.1:8000`
* Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## Running with Next.js Frontend

In the root directory:

```bash
# Terminal 1: Next.js Frontend
npm run dev

# Terminal 2: FastAPI Backend
npm run backend:dev
```
