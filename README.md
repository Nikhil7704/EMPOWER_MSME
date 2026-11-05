# EmpowerMSME - Full-Stack & Decoupled Financial Ecosystem for Indian MSMEs

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-16.1-black?logo=next.js)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![LangChain](https://img.shields.io/badge/LangChain-Python-1C3C3C?logo=chainlink&logoColor=white)](https://python.langchain.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-4.1-38B2AC?logo=tailwind-css)](https://tailwindcss.com)

> An inclusive digital financial platform connecting MSMEs with investors, lenders, and government schemes across India — powered by a **decoupled Next.js 16 frontend** and a **high-performance Python FastAPI backend**.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [User Roles](#user-roles)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference & Swagger Docs](#api-reference--swagger-docs)
- [AI & ML Features](#ai-features)
- [Scripts](#scripts)
- [Deployment](#deployment)

---

## Overview

**EmpowerMSME** is a production-grade, full-stack financial technology ecosystem designed to democratize access to financial services for Micro, Small, and Medium Enterprises (MSMEs) across India. The platform bridges the gap between MSME owners, individual investors, and institutional lenders through a transparent, technology-driven marketplace.

### Problems it solves

- MSMEs struggle to access formal credit due to lack of verifiable credit history
- Investors have no curated marketplace to discover verified MSME investment opportunities
- Traditional lending is opaque, slow, and excludes small businesses
- Financial literacy regarding government subsidy schemes is limited

---

## Architecture

The platform uses a modern, decoupled microservice-ready architecture:

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

* **Frontend:** Built with Next.js 16 (App Router), React 19, Tailwind CSS v4, and Radix UI / shadcn components.
* **Backend:** Asynchronous Python FastAPI backend with Pydantic v2 schemas, SQLAlchemy 2.0 ORM, and automated OpenAPI documentation at `http://127.0.0.1:8000/docs`.
* **AI/RAG:** Python LangChain & Google Gemini 1.5 Flash/Pro with semantic vector search over official Indian MSME schemes.

---

## Features

### For Business Owners (MSME Role)

| Feature | Description |
|---|---|
| Business Dashboard | Real-time KPIs — revenue, active loans, funding raised, credit score gauge |
| Loan Applications | Apply for loans, track lifecycle (Submitted to Disbursed), upload documents |
| Campaign Management | Create fundraising campaigns, set funding goals, track investor engagement |
| AI Credit Scoring Engine | 7-factor transparent credit evaluation (300–900 scale) with full explainability |
| Revenue-Based Financing (RBF) | Alternative financing with interactive sliders and RBF vs EMI comparison |
| P2P Lending Circles | Community-based group savings and fund rotation with trust scores |
| Repayments Dashboard | EMI tracking, balance trend charts, overdue alerts, payment history |
| AI Story Builder | Generate 3 pitch variants (Professional, Emotional, Data-Driven) |
| AI Knowledge Academy | RAG-powered chatbot covering MUDRA, PMEGP, GST, SIDBI schemes |
| Business Analytics | Revenue trends, loan volume charts, sector distribution |
| Profile and KYC | Business profile management, document uploads, KYC status |

### For Investors (Individual Role)

| Feature | Description |
|---|---|
| Investor Dashboard | Portfolio value, total invested, active investments, avg ROI, cumulative chart |
| Browse Campaigns | Discover MSME investment opportunities with sector/risk filters |
| Invest in Businesses | One-click invest dialog with amount entry and risk summary |
| Portfolio Analytics | Investment history, ROI tracking, portfolio growth visualization |
| Explore Businesses | Browse verified MSME business profiles with search and filters |
| Applications | View and track investment applications |
| Academy | Educational content on MSME investing and government schemes |

### For Platform Administrators

| Feature | Description |
|---|---|
| Admin Dashboard | Platform-wide KPIs — total users, businesses, loans, investments |
| User Management | View all users, approve/reject KYC, manage roles |
| Business Verification | Review and verify MSME business profiles and KYC documents |
| Loan Management | View all loan applications, update status |
| Campaign Oversight | Monitor active campaigns, flag suspicious activity |
| Platform Analytics | User growth charts, loan volume trends, default rates |
| Audit Logs | Immutable audit trail — Auth, Financial, KYC, Security events |
| Security Console | Live login activity tracker, MFA controls |

---

## Tech Stack

### Frontend (Next.js)

| Technology | Version | Purpose |
|---|---|---|
| Next.js | 16.1.6 | Full-stack React framework with App Router and Turbopack |
| React | 19.2.0 | UI component library |
| Tailwind CSS | 4.1.9 | Utility-first styling |
| shadcn/ui | Latest | Pre-built accessible UI components (Radix UI based) |
| Framer Motion | 12.38 | Animations, page transitions, spring physics |
| Recharts | 2.15.4 | Data visualization — area, bar, pie, line charts |
| Lucide React | 0.454 | Icon library |

### Backend (Python FastAPI)

| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.115+ | High-performance asynchronous Python web framework |
| Uvicorn | 0.32+ | ASGI web server |
| Pydantic | 2.9+ | Data validation and schema enforcement |
| SQLAlchemy | 2.0+ | Object Relational Mapper for relational databases |
| Alembic | 1.13+ | Database schema migrations |
| python-jose | 3.3+ | JWT token generation and verification |
| bcrypt | 5.0+ | Secure password salt hashing |

### AI and Machine Learning

| Technology | Purpose |
|---|---|
| LangChain Python | RAG pipeline orchestration and prompt chains |
| @langchain/google-genai | Google Gemini AI integration (embeddings & generation) |
| Semantic Knowledge Base | Curated MSME knowledge base on MUDRA, PMEGP, GST, SIDBI |
| 7-Factor Weighted Model | Interpretable, transparent credit scoring algorithm |

---

## Project Structure

```text
Empower_MSME/
├── app/                          # Next.js 16 Frontend (App Router)
│   ├── page.jsx                  # Public landing page
│   ├── marketplace/              # Browse MSME campaigns
│   ├── business/                 # MSME Owner Portal
│   ├── user/                     # Investor Portal
│   ├── admin/                    # Platform Admin Portal
│   └── api/                      # Next.js Route Handlers
├── backend/                      # Python FastAPI Backend
│   ├── app/
│   │   ├── api/                  # FastAPI Endpoints (auth, loans, campaigns, etc.)
│   │   ├── core/                 # Config, Database Session, JWT Security
│   │   ├── models/               # SQLAlchemy Models (User, Loan, Campaign, etc.)
│   │   ├── schemas/              # Pydantic v2 Request/Response Schemas
│   │   ├── services/             # Credit Engine, RAG Pipeline, Audit Logger
│   │   └── main.py               # FastAPI App Assembly & Middleware
│   ├── seed.py                   # Demo database seeder
│   ├── test_api.py               # 12 Automated integration test suites
│   ├── run.py                    # Server startup script
│   └── requirements.txt          # Python dependencies
├── components/                   # Reusable UI & Widget components
├── lib/                          # Client utilities and auth context
├── prisma/                       # Prisma Schema (fallback/dev)
└── package.json
```

---

## Getting Started

### Prerequisites

- **Node.js:** v18 or higher — https://nodejs.org
- **Python:** 3.11 or 3.12 — https://python.org
- **Git**

---

### 1. Clone the repository

```bash
git clone https://github.com/Nikhil7704/EMPOWER_MSME.git
cd EMPOWER_MSME
```

---

### 2. Frontend Setup (Next.js)

```bash
# Install frontend dependencies
npm install

# Start Next.js development server
npm run dev
```

The frontend will run at `http://localhost:3000`.

---

### 3. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install Python requirements
pip install -r requirements.txt

# Seed the database with demo accounts
python seed.py

# Run automated tests
python test_api.py

# Launch FastAPI server
python run.py
```

* **FastAPI Server:** `http://127.0.0.1:8000`
* **Interactive Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc Documentation:** `http://127.0.0.1:8000/redoc`

#### Demo Accounts (Pre-configured):
| Role | Email | Password |
|---|---|---|
| Business | `business@demo.com` | `demo1234` |
| Investor | `investor@demo.com` | `demo1234` |
| Admin | `admin@demo.com` | `demo1234` |

---

## Environment Variables

Create a `.env` file in the root directory:

```env
# NextAuth / JWT Secret
NEXTAUTH_SECRET="your-random-secret-key-minimum-32-characters"
NEXTAUTH_URL="http://localhost:3000"

# Database connection string
DATABASE_URL="file:./prisma/dev.db"

# Optional: Google Gemini API key for AI RAG chatbot
GEMINI_API_KEY="your-google-gemini-api-key"
```

---

## API Reference & Swagger Docs

The FastAPI backend automatically generates interactive Swagger OpenAPI documentation accessible live at `http://127.0.0.1:8000/docs`.

### Key Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new business or investor user |
| `POST` | `/api/auth/login` | Login and receive JWT access token |
| `GET` | `/api/auth/me` | Retrieve profile and permissions of authenticated user |
| `GET` | `/api/loans` | List business loans or filter by loan ID |
| `POST` | `/api/loans` | Submit a new loan application |
| `GET` | `/api/campaigns` | Browse fundraising campaigns (filter by sector/region) |
| `POST` | `/api/campaigns` | Launch a fundraising campaign |
| `POST` | `/api/campaigns/invest` | Invest in an active MSME campaign |
| `GET` | `/api/repayments` | View EMI amortization ledger and upcoming dues |
| `POST` | `/api/repayments` | Record an EMI repayment transaction |
| `GET` | `/api/credit/evaluate` | Get credit engine scoring weights and risk tiers |
| `POST` | `/api/credit/evaluate` | Run 7-factor transparent credit scoring evaluation |
| `GET` | `/api/lending-circles` | List community P2P lending circles |
| `POST` | `/api/lending-circles` | Create or join a mutual lending circle |
| `GET` | `/api/analytics/business` | MSME revenue trends, funding progress, and loan health |
| `GET` | `/api/analytics/user` | Investor portfolio value, ROI, and distributions |
| `GET` | `/api/admin/users` | Admin KYC review and user management |
| `POST` | `/api/chat` | Query the LangChain + Gemini RAG knowledge assistant |

---

## AI Features

### 1. Credit Scoring Engine (`/api/credit/evaluate`)
A fully transparent, explainable weighted linear model that scores businesses on alternative financial indicators:

| Factor | Weight | Description |
|---|---|---|
| Repayment History | 25% | Past loan repayment track record |
| Annual Revenue | 20% | Business turnover scale |
| Net Profit Margin | 15% | Profitability percentage |
| Cash Flow Stability | 15% | Inverse of monthly revenue variance |
| Debt-to-Income | 10% | Existing debt relative to revenue |
| Business Age | 10% | Years in operation |
| GST Filing Consistency | 5% | Timeliness of GST return filings |

### 2. AI Knowledge Academy (RAG Pipeline)
RAG-powered conversational assistant using LangChain and Google Gemini over official Indian MSME schemes:
* MUDRA Loans (Shishu, Kishore, Tarun)
* PMEGP (Prime Minister's Employment Generation Programme)
* GST Registration & Composition Scheme
* SIDBI Development Schemes
* Revenue-Based Financing models

### 3. AI Story Builder
Automatically synthesizes business financial metrics into 3 distinct fundraising pitch variations:
* **Professional:** Formal investor-facing deck with projected ROI.
* **Emotional:** Grassroots community impact and job creation narrative.
* **Data-Driven:** Pure metrics, margin profiles, and payback horizons.

---

## Scripts

```bash
# Run Next.js Frontend
npm run dev

# Run Python FastAPI Backend
npm run backend:dev

# Seed FastAPI Database with Demo Users
npm run backend:seed

# Run FastAPI 12-Point Automated Integration Tests
npm run backend:test

# Build Next.js for Production
npm run build
```

---

## License

This project is licensed under the MIT License.

---

**EmpowerMSME** — Empowering India's grassroots enterprises through transparent technology and inclusive capital.
