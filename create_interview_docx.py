import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = docx.Document()

    # Page setup - Margins 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._element.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_title(text, subtitle_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129)

        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(20)
        run2 = p2.add_run(subtitle_text)
        run2.font.name = 'Calibri'
        run2.font.size = Pt(13)
        run2.font.italic = True
        run2.font.color.rgb = RGBColor(100, 100, 100)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        # Add a bottom border line
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(40, 116, 166)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(52, 73, 94)
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(33, 33, 33)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.italic = italic
        run.font.color.rgb = RGBColor(44, 62, 80)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(33, 33, 33)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(44, 62, 80)
        return p

    def add_callout(text, title=None, callout_type="note"):
        colors = {
            "note": ("EBF5FB", "2980B9"),
            "warning": ("FEF9E7", "F39C12"),
            "tip": ("E8F8F5", "1ABC9C"),
            "qa": ("F4ECF7", "8E44AD"),
            "danger": ("FDEDEC", "E74C3C"),
        }
        bg_hex, border_hex = colors.get(callout_type, colors["note"])

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15

        if title:
            r_title = p.add_run(f"{title}\n")
            r_title.font.name = 'Calibri'
            r_title.font.size = Pt(11)
            r_title.font.bold = True
            r_title.font.color.rgb = RGBColor.from_string(border_hex)

        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(44, 62, 80)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F2F4F4")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0

        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(33, 47, 61)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_qa(q_num, question, answer, key_concepts=None, code_snippet=None, follow_up=None):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(14)
        p_q.paragraph_format.space_after = Pt(4)
        p_q.paragraph_format.keep_with_next = True

        r_num = p_q.add_run(f"Q{q_num}: ")
        r_num.font.name = 'Calibri'
        r_num.font.size = Pt(12.5)
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(142, 68, 173)

        r_q = p_q.add_run(question)
        r_q.font.name = 'Calibri'
        r_q.font.size = Pt(12.5)
        r_q.font.bold = True
        r_q.font.color.rgb = RGBColor(44, 62, 80)

        if key_concepts:
            add_p(key_concepts, bold_prefix="Key Concepts Tested: ", italic=True)

        add_p(answer, bold_prefix="Interview Answer: ")

        if code_snippet:
            add_code_block(code_snippet)

        if follow_up:
            add_p(follow_up, bold_prefix="Possible Follow-Up: ", italic=True)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_table_with_data(headers, data, col_widths=None):
        """Helper to create a formatted table"""
        table = doc.add_table(rows=1 + len(data), cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        for i, h in enumerate(headers):
            cell = table.cell(0, i)
            set_cell_background(cell, "0F4C81")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(h)
            r.font.name = 'Calibri'
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

        for row_idx, row_data in enumerate(data):
            bg = "F8F9F9" if row_idx % 2 == 0 else "FFFFFF"
            for col_idx, text in enumerate(row_data):
                cell = table.cell(row_idx + 1, col_idx)
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                r = p.add_run(str(text))
                r.font.name = 'Calibri'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(44, 62, 80)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        return table

    # =============================================================
    # DOCUMENT CONTENT GENERATION
    # =============================================================

    add_title(
        "EmpowerMSME — Complete Interview Preparation Master Guide",
        "Project Deep Dive: Motivation, Architecture, Implementation, Challenges, Features & 40+ Interview Q&A"
    )

    # EXECUTIVE SUMMARY BOX
    add_callout(
        "This guide is your single source of truth for interview preparation on the EmpowerMSME project. "
        "It covers exactly what the project is, why you built it, every architectural decision and its justification, "
        "real problems you faced during development and how you solved them, all features implemented with their technical depth, "
        "what can be improved, how the database works, and 40+ interview questions with detailed answers. "
        "The backend is presented as Python FastAPI with async architecture — no frontend questions included.",
        title="HOW TO USE THIS GUIDE",
        callout_type="note"
    )

    # =========================================================================
    # SECTION 1: WHAT IS THIS PROJECT & WHY I BUILT IT
    # =========================================================================
    add_h1("1. What is EmpowerMSME — The Complete Picture")

    add_h2("1.1 The Elevator Pitch (30-Second Answer)")
    add_callout(
        "EmpowerMSME is a full-stack digital financial ecosystem that I built to bridge the formal credit gap "
        "for Micro, Small, and Medium Enterprises (MSMEs) in India. It connects MSME business owners with individual "
        "and institutional investors through a transparent, AI-driven marketplace. The platform provides loan management, "
        "crowdfunding campaigns, an AI-powered credit scoring engine, a RAG-based chatbot for government scheme discovery, "
        "P2P lending circles, and comprehensive admin oversight — all backed by a relational database with full ACID compliance.",
        title="YOUR 30-SECOND PITCH",
        callout_type="tip"
    )

    add_h2("1.2 Why I Built This — The Motivation")
    add_p("India has over 63 million MSMEs contributing ~30% of GDP, yet more than 80% of them have zero access to formal banking credit. "
          "I saw this as a massive technology gap — not a lack of viable businesses, but a lack of digital infrastructure to evaluate them fairly. "
          "Traditional banks reject MSME applications because they lack CIBIL scores, audited financial statements, or collateral.")
    add_p("I wanted to solve this from first principles:")
    add_bullet("Build a transparent credit scoring system that doesn't rely on CIBIL — using the business's own operational data (revenue, GST filings, repayment history).", bold_prefix="Problem 1 → Solution: ")
    add_bullet("Create a marketplace where investors can discover verified MSME businesses with transparent risk ratings, so small businesses get funded by real people, not just banks.", bold_prefix="Problem 2 → Solution: ")
    add_bullet("Offer Revenue-Based Financing (RBF) as an alternative to rigid EMI — if a seasonal business earns less one month, they pay less. No defaults, no stress.", bold_prefix="Problem 3 → Solution: ")
    add_bullet("Build a RAG-powered AI chatbot that helps MSME owners navigate complex government schemes (MUDRA, PMEGP, SIDBI, Stand-Up India) — because information asymmetry is a real barrier.", bold_prefix="Problem 4 → Solution: ")

    add_h2("1.3 Who Uses This Platform? (User Roles)")
    add_table_with_data(
        ["User Role", "What They Do", "Key Features They Access"],
        [
            ("MSME Business Owner", "Applies for loans, creates fundraising campaigns, checks AI credit score, manages repayments, gets scheme guidance from chatbot",
             "Dashboard, Loans, Campaigns, Credit Score Engine, RBF Slider, Lending Circles, AI Academy Chatbot, Story Builder, Analytics, Repayments"),
            ("Investor (Individual/Institutional)", "Discovers MSME investment opportunities, invests in campaigns, tracks portfolio ROI and returns",
             "Campaign Discovery, 1-Click Invest, Portfolio Analytics, ROI Tracking, Business Explorer"),
            ("Platform Administrator", "Verifies businesses (KYC), approves loans, monitors platform health, reviews audit logs",
             "User Management, Business Verification, Loan Approvals, Platform Analytics, Audit Logs, Security Console, Platform Settings"),
        ]
    )

    add_h2("1.4 What Makes This Project Non-Trivial")
    add_p("This isn't a simple CRUD app. Here's what makes it complex:")
    add_bullet("A custom 7-factor weighted linear credit scoring algorithm with full explainability — every factor contribution is transparent.", bold_prefix="AI Credit Scoring Engine: ")
    add_bullet("Investment into campaigns uses database transactions to atomically update both the Investment record and the Campaign's raised balance — preventing race conditions where two investors overfund a campaign.", bold_prefix="Atomic Financial Transactions: ")
    add_bullet("LangChain + Google Gemini 1.5 Pro + custom in-memory vector store with cosine similarity retrieval — not just keyword matching, but semantic understanding of user queries against a curated knowledge base of Indian MSME schemes.", bold_prefix="RAG Pipeline (Retrieval-Augmented Generation): ")
    add_bullet("Three distinct user portals (Business, Investor, Admin) with role-based middleware protection — each portal has 10-15 pages with different data access patterns.", bold_prefix="Multi-Role Architecture: ")
    add_bullet("9 interconnected database tables with foreign key constraints, cascade deletes, and JSONB metadata — a genuinely relational financial data model.", bold_prefix="Complex Relational Schema: ")

    # =========================================================================
    # SECTION 2: COMPLETE FEATURE LIST
    # =========================================================================
    add_h1("2. All Features Implemented — Complete Breakdown")

    add_h2("2.1 Business Owner Features")
    features_business = [
        ("Business Dashboard", "Real-time KPI cards showing revenue, active loans, funding raised, and a live AI credit score gauge (SVG semicircle 300-900)"),
        ("Loan Applications", "Full loan lifecycle: Submit → Under Review → Approved → Disbursed. Each loan tracks amount, interest rate, tenure, EMI, bank details, and linked repayment schedule"),
        ("Campaign Management", "Create fundraising campaigns with goal amount, risk rating, ROI %, repayment model. Campaigns go through pending → active → funded → expired states"),
        ("AI Credit Scoring Engine", "7-factor weighted scoring (300-900). Factors: Annual Revenue (20%), Repayment History (20%), Net Profit Margin (15%), Cash Flow Stability (15%), Debt-to-Income (15%), Business Age (10%), GST Filing (5%). Returns score, risk category, eligibility tier, recommended loan amount, interest rate, and human-readable improvement tips"),
        ("Revenue-Based Financing (RBF)", "Interactive sliders to compare RBF vs Fixed EMI repayment. RBF charges 8% of monthly revenue instead of fixed EMI — adapts to seasonal cash flow"),
        ("P2P Lending Circles", "Digital ROSCA (Rotating Savings and Credit Association). Members contribute monthly, one member receives the pool each round. Trust scores track contribution reliability"),
        ("Repayments Dashboard", "EMI tracker with paid/upcoming/missed status per month. Balance trend charts. Overdue alerts. Both EMI and RBF repayment views"),
        ("AI Story Builder", "Generates 3 pitch variants from business data: Professional (investor-facing), Emotional (human-interest), Data-Driven (metrics-focused)"),
        ("AI Knowledge Academy", "RAG-powered chatbot covering MUDRA, PMEGP, GST, SIDBI, Udyam Registration, Working Capital, Credit Score Improvement, Stand-Up India, ECLGS, P2P Lending regulations"),
        ("Business Analytics", "Revenue trends, loan volume charts, sector distribution visualization"),
    ]
    for name, desc in features_business:
        add_bullet(desc, bold_prefix=f"{name}: ")

    add_h2("2.2 Investor Features")
    features_investor = [
        ("Investor Dashboard", "Portfolio value, total invested across campaigns, active investment count, average ROI, cumulative growth chart"),
        ("Campaign Discovery", "Browse active MSME campaigns with filters: sector, region, risk level, status. Each campaign shows business name, funding progress, ROI, repayment model"),
        ("1-Click Investment", "Invest dialog with amount entry, risk summary, and campaign details. Investment executes as an atomic database transaction"),
        ("Portfolio Analytics", "Investment history timeline, ROI per campaign, portfolio diversification by sector, monthly return tracking"),
        ("Business Explorer", "Browse verified MSME profiles with search and filtering by sector, location, credit score range"),
    ]
    for name, desc in features_investor:
        add_bullet(desc, bold_prefix=f"{name}: ")

    add_h2("2.3 Admin Features")
    features_admin = [
        ("Admin Dashboard", "Platform-wide KPIs: total users, registered businesses, active loans, total investments, default rates"),
        ("User Management", "View all users, filter by role, approve/reject KYC status, manage roles"),
        ("Business Verification", "Review MSME business profiles, verify Udyam registration, approve/reject KYC documents"),
        ("Loan Management", "View all loan applications across the platform, update status (approve/reject/disburse)"),
        ("Campaign Oversight", "Monitor active campaigns, flag suspicious activity, moderate campaign content"),
        ("Platform Analytics", "User growth charts, loan volume trends, investment flows, default rate monitoring"),
        ("Audit Logs", "Immutable audit trail with categories: Auth, Financial, KYC, Security. Each entry: action, user email, IP address, status (success/warning/danger/info), metadata JSON, timestamp"),
        ("Security Console", "Live login activity tracker, session monitoring"),
        ("Platform Settings", "Global configuration: fee rates, platform parameters, system settings"),
    ]
    for name, desc in features_admin:
        add_bullet(desc, bold_prefix=f"{name}: ")

    add_h2("2.4 Public Features")
    add_bullet("Hero section with animated statistics, features overview, testimonials, CTA sections", bold_prefix="Landing Page: ")
    add_bullet("Public MSME business listing with search and sector filters — no login required", bold_prefix="Marketplace: ")
    add_bullet("Rule-based analysis engine that detects financial fraud patterns in SMS messages", bold_prefix="SMS Spam Checker: ")
    add_bullet("RAG-powered educational content on government schemes — accessible without login", bold_prefix="Academy: ")

    # =========================================================================
    # SECTION 3: ARCHITECTURE & TECH STACK
    # =========================================================================
    add_h1("3. System Architecture & Tech Stack")

    add_h2("3.1 Architecture Overview")
    add_p("The system follows a layered, API-driven architecture with clear separation of concerns:")
    add_bullet("Python 3.11+ with FastAPI framework running on Uvicorn ASGI server. Fully asynchronous request handling with async/await pattern. Automatic OpenAPI/Swagger documentation. Pydantic models for strict request/response validation.", bold_prefix="Backend API Layer (FastAPI): ")
    add_bullet("PostgreSQL 15 for production (SQLite for local development). Prisma ORM for type-safe database access, schema management, and migrations. 9 interconnected models with foreign key constraints and cascade deletes.", bold_prefix="Database Layer: ")
    add_bullet("LangChain orchestrating RAG pipeline. Google Gemini 1.5 Pro as the LLM. text-embedding-004 model generating 768-dimensional embeddings. Custom in-memory vector store with cosine similarity retrieval.", bold_prefix="AI/ML Layer: ")
    add_bullet("NextAuth.js with JWT strategy. bcryptjs (12 rounds) for password hashing. Role-based middleware protection. 30-day session with httpOnly cookies.", bold_prefix="Authentication & Security Layer: ")

    add_h2("3.2 Tech Stack — Complete Table")
    add_table_with_data(
        ["Layer", "Technology", "Version", "Purpose & Why I Chose It"],
        [
            ("Runtime", "Python 3.11+", "3.11+", "Async support, type hints, FastAPI compatibility, rich AI/ML ecosystem"),
            ("Framework", "FastAPI", "Latest", "Async-native, automatic Swagger docs, Pydantic validation, Depends() DI, on par with Node.js/Go performance"),
            ("ASGI Server", "Uvicorn", "Latest", "Lightning-fast ASGI server, non-blocking event loop, handles concurrent connections efficiently"),
            ("ORM", "Prisma (via Prisma Client)", "6.19.3", "Type-safe queries, auto-generated client, schema-first design, built-in migrations"),
            ("Database (Dev)", "SQLite", "3.x", "Zero-config local development, file-based, instant setup with Prisma"),
            ("Database (Prod)", "PostgreSQL", "15+", "ACID compliance, JSONB support, foreign keys, row-level locking, Write-Ahead Logging"),
            ("Authentication", "JWT + bcryptjs", "—", "Stateless auth, 30-day sessions, HMAC-SHA256 signature, httpOnly cookies"),
            ("AI/LLM", "Google Gemini 1.5 Pro", "1.5", "High-quality generation, 1M token context, integrated with LangChain"),
            ("Embeddings", "text-embedding-004", "—", "768-dimensional vectors, optimized for semantic similarity search"),
            ("RAG Framework", "LangChain", "1.5.3", "LCEL pipeline composition, prompt templates, output parsers, runnable sequences"),
            ("Validation", "Pydantic", "v2", "Strict runtime type checking, automatic JSON schema generation, custom validators"),
            ("Password Hashing", "bcryptjs", "3.0.3", "Adaptive cost factor (12 rounds = 4096 iterations), automatic salt generation"),
        ]
    )

    add_h2("3.3 Why FastAPI? — Architecture Justification")
    add_callout(
        "Interview Tip: When asked 'Why did you choose FastAPI?', don't just say 'it's fast'. "
        "Talk about async I/O for concurrent DB queries, Pydantic for automatic validation (no manual error checking), "
        "Dependency Injection for clean auth guards, and native Python for seamless LangChain/AI integration.",
        title="INTERVIEW TIP",
        callout_type="warning"
    )
    add_bullet("FastAPI is built on Starlette (ASGI) and runs on an async event loop via Uvicorn. This means when one request is waiting for a database response (I/O), the event loop can serve other requests instead of blocking. This is critical for a financial platform where multiple investors may be submitting investments simultaneously.", bold_prefix="Async-Native Performance: ")
    add_bullet("Every request body is automatically validated against a Pydantic schema before it reaches my business logic. If a field is missing or has the wrong type, FastAPI returns a 422 Unprocessable Entity with detailed error messages — zero manual validation code needed.", bold_prefix="Pydantic Auto-Validation: ")
    add_bullet("FastAPI's Depends() system lets me inject database sessions, authentication tokens, and role checks as function parameters. This keeps my route handlers clean and my auth logic reusable across 12+ API endpoints.", bold_prefix="Dependency Injection: ")
    add_bullet("Since I'm using LangChain, Gemini SDK, NumPy, and custom scoring algorithms — all Python libraries — FastAPI gives me native access without any cross-language bridges. The credit scoring engine, RAG pipeline, and API handlers all share the same Python runtime.", bold_prefix="Python AI/ML Ecosystem: ")

    add_h2("3.4 Why PostgreSQL? — Database Justification")
    add_bullet("Investment creation + campaign balance update must happen atomically. If the investment record is created but the campaign.raised update fails, the entire transaction rolls back. PostgreSQL guarantees this with proper ACID transactions.", bold_prefix="ACID Transactions for Financial Data: ")
    add_bullet("Every Investment must reference a valid Campaign and User. Every Loan must reference a valid BusinessProfile. Cascade deletes ensure no orphaned records. This relational integrity is impossible to enforce reliably in document databases like MongoDB.", bold_prefix="Foreign Key Constraints: ")
    add_bullet("KYC documents metadata, audit log metadata, and campaign filtering parameters are stored as JSONB — giving me NoSQL-like flexibility for semi-structured data inside a relational database.", bold_prefix="JSONB for Semi-Structured Data: ")
    add_bullet("For concurrent investments, I can use SELECT FOR UPDATE to lock a campaign row, preventing two investors from simultaneously overfunding a campaign beyond its goal.", bold_prefix="Row-Level Locking: ")

    # =========================================================================
    # SECTION 4: DATABASE DEEP DIVE
    # =========================================================================
    add_h1("4. Database Design — Schema, Relationships & How It Works")

    add_h2("4.1 Entity-Relationship Overview")
    add_p("The database has 9 interconnected models. Here's the complete schema with relationships:")

    add_h3("Model 1: User (Core Authentication Entity)")
    add_code_block(
        "model User {\n"
        "  id              String    @id @default(uuid())\n"
        "  email           String    @unique\n"
        "  passwordHash    String\n"
        "  role            String    // 'BUSINESS' | 'INVESTOR' | 'ADMIN'\n"
        "  kycStatus       String    @default('PENDING')  // 'PENDING' | 'VERIFIED' | 'REJECTED'\n"
        "  createdAt       DateTime  @default(now())\n"
        "  updatedAt       DateTime  @updatedAt\n"
        "  businessProfile BusinessProfile?    // 1:1 (only for BUSINESS role)\n"
        "  investments     Investment[]         // 1:Many (only for INVESTOR role)\n"
        "  auditLogs       AuditLog[]           // 1:Many\n"
        "  circleMembers   LendingCircleMember[] // 1:Many\n"
        "}"
    )
    add_p("The User model is the central authentication entity. The role field determines which portal they access. "
          "A BUSINESS user has a 1:1 BusinessProfile. An INVESTOR user has many Investments. All users generate AuditLog entries.")

    add_h3("Model 2: BusinessProfile (MSME Business Data)")
    add_code_block(
        "model BusinessProfile {\n"
        "  id           String     @id @default(uuid())\n"
        "  userId       String     @unique\n"
        "  user         User       @relation(fields: [userId], references: [id], onDelete: Cascade)\n"
        "  name         String\n"
        "  sector       String\n"
        "  location     String\n"
        "  udyamId      String     @unique    // Government MSME registration ID\n"
        "  employees    Int\n"
        "  businessAge  Float\n"
        "  description  String\n"
        "  fundingGoal  Float\n"
        "  creditScore  Int        @default(300)  // 300-900 range\n"
        "  kycDocs      String     @default('[]') // JSON string for document metadata\n"
        "  campaigns    Campaign[]\n"
        "  loans        Loan[]\n"
        "}"
    )
    add_p("Key design decisions: udyamId is @unique because every registered MSME in India has a unique Udyam number. "
          "creditScore defaults to 300 (minimum) — it's updated when the AI scoring engine runs. "
          "kycDocs stores document metadata as a JSON string (SQLite compatibility; would be JSONB in PostgreSQL).")

    add_h3("Model 3: Campaign (Fundraising Campaigns)")
    add_p("Campaigns link a BusinessProfile to investment opportunities. Status lifecycle: pending → active → funded → expired. "
          "The 'raised' field is atomically incremented during investment transactions.")

    add_h3("Model 4: Investment (Investor → Campaign)")
    add_p("Each Investment links an Investor (User) to a Campaign. Uses Prisma's $transaction to atomically create the Investment record AND increment Campaign.raised. "
          "Status: active → completed → defaulted.")

    add_h3("Model 5: Loan (Loan Applications)")
    add_p("Full loan lifecycle tracking. Platform automatically calculates platformFee (2% of loan amount). "
          "Status: pending → approved → disbursed → repaid. Each loan links to a RepaymentLedger for EMI tracking.")

    add_h3("Model 6: RepaymentLedger (EMI Tracking)")
    add_p("Each entry represents one monthly installment. Tracks dueDate, amountDue, amountPaid, status (pending/paid/missed), and actual paidDate. "
          "Generated automatically when a loan is disbursed — creates N entries for N tenure months.")

    add_h3("Model 7-8: LendingCircle & LendingCircleMember")
    add_p("Digital ROSCA implementation. LendingCircle defines the group (contribution amount, frequency, max members, current round). "
          "LendingCircleMember tracks each participant's contribution status and trust score (0-100).")

    add_h3("Model 9: AuditLog (Immutable Event Trail)")
    add_code_block(
        "model AuditLog {\n"
        "  id        String   @id @default(uuid())\n"
        "  action    String           // 'user_login', 'loan_approved', 'kyc_verified', etc.\n"
        "  userEmail String\n"
        "  userId    String?\n"
        "  user      User?    @relation(fields: [userId], references: [id], onDelete: SetNull)\n"
        "  ipAddress String\n"
        "  category  String           // 'Auth' | 'KYC' | 'Financial' | 'Security'\n"
        "  status    String           // 'success' | 'warning' | 'danger' | 'info'\n"
        "  metadata  String?          // Stringified JSON with additional context\n"
        "  timestamp DateTime @default(now())\n"
        "}"
    )
    add_p("Note: onDelete: SetNull on the user relation means if a user is deleted, their audit logs are preserved (userId becomes null) — "
          "audit records are immutable and must never be lost.")

    add_h2("4.2 Key Relationship Chains")
    add_p("Understanding these chains is critical for interviews:")
    add_bullet("User (1:1) → BusinessProfile (1:Many) → Campaign (1:Many) → Investment (Many:1) ← User", bold_prefix="Investment Chain: ")
    add_bullet("User (1:1) → BusinessProfile (1:Many) → Loan (1:Many) → RepaymentLedger", bold_prefix="Loan Lifecycle Chain: ")
    add_bullet("LendingCircle (1:Many) → LendingCircleMember (Many:1) ← User", bold_prefix="P2P Circle Chain: ")

    # =========================================================================
    # SECTION 5: HOW KEY FEATURES WORK — IMPLEMENTATION DEEP DIVE
    # =========================================================================
    add_h1("5. How Key Features Work — Implementation Deep Dive")

    add_h2("5.1 Authentication Flow — How Login Works End-to-End")
    add_p("1. User submits email + password to POST /api/auth/register.\n"
          "2. Server checks if email already exists in database (findUnique).\n"
          "3. Password is hashed using bcryptjs with 10 salt rounds: bcrypt.hash(password, 10).\n"
          "4. If role is BUSINESS, user AND business profile are created in a single Prisma nested write (atomic).\n"
          "5. For login, NextAuth's CredentialsProvider calls authorize() — fetches user by email, compares hash with bcrypt.compare().\n"
          "6. On success, JWT token is generated containing: id, email, role, kycStatus.\n"
          "7. JWT is stored in an httpOnly cookie with 30-day expiry.\n"
          "8. middleware.js intercepts all requests to /business/*, /user/*, /admin/* — checks JWT token and validates role matches the route prefix.\n"
          "9. If role mismatch, user is redirected to /auth/select.")

    add_code_block(
        "# Authentication Middleware (FastAPI equivalent of middleware.js)\n"
        "# Checks JWT token and enforces role-based route protection\n\n"
        "async def get_current_user(token: str = Depends(oauth2_scheme)):\n"
        "    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\n"
        "    user_id = payload.get('sub')\n"
        "    role = payload.get('role')\n"
        "    if not user_id:\n"
        "        raise HTTPException(status_code=401, detail='Invalid token')\n"
        "    return {'id': user_id, 'role': role}\n\n"
        "def require_role(required_role: str):\n"
        "    def role_checker(current_user = Depends(get_current_user)):\n"
        "        if current_user['role'] != required_role:\n"
        "            raise HTTPException(status_code=403, detail='Insufficient permissions')\n"
        "        return current_user\n"
        "    return role_checker"
    )

    add_h2("5.2 Credit Scoring Engine — The Algorithm")
    add_p("This is the most technically interesting feature. Here's the exact algorithm:")
    add_code_block(
        "WEIGHTS = {\n"
        "    'annualRevenue':       0.20,  # Business viability\n"
        "    'netProfitMargin':     0.15,  # Profitability\n"
        "    'cashFlowStability':   0.15,  # Lower variance = better\n"
        "    'debtToIncome':        0.15,  # Lower ratio = better (inverted)\n"
        "    'repaymentHistory':    0.20,  # Past behavior — highest weight\n"
        "    'businessAge':         0.10,  # Credibility\n"
        "    'gstFilingConsistency':0.05,  # Regulatory compliance\n"
        "}\n\n"
        "# Step 1: Normalize each factor to 0-1 range\n"
        "revenueScore    = normalize(annualRevenue, 0, 10_000_000)\n"
        "profitScore     = normalize(netProfitMargin, -20, 40)\n"
        "cashFlowScore   = 1 - normalize(cashFlowVariance, 0, 60)  # inverted\n"
        "debtScore       = 1 - normalize(debtRatio, 0, 2.5)         # inverted\n"
        "repaymentScore  = normalize(repaymentHistory, 0, 100)\n"
        "ageScore        = normalize(businessAge, 0, 10)\n"
        "gstScore        = normalize(gstFilingScore, 0, 100)\n\n"
        "# Step 2: Compute weighted sum\n"
        "weightedSum = sum(score * weight for score, weight in zip(scores, weights))\n\n"
        "# Step 3: Apply industry risk penalty\n"
        "penalty = {'low': 0, 'medium': 0.04, 'high': 0.12}\n"
        "weightedSum = clamp(weightedSum - penalty[industryRisk])\n\n"
        "# Step 4: Map to 300-900 range\n"
        "creditScore = 300 + weightedSum * 600"
    )
    add_p("The engine also returns: riskCategory (Low/Medium/High), eligibilityTier (Excellent/Good/Fair/Poor), "
          "recommendedLoanAmount (based on revenue × multiplier), suggested interestRate, per-factor contribution percentages, "
          "and human-readable positives and improvement suggestions.")

    add_h2("5.3 Investment Transaction — Atomic Database Operation")
    add_p("This is the most critical financial operation in the system:")
    add_code_block(
        "# Actual implementation using Prisma's $transaction\n"
        "# Both operations succeed or both rollback — no partial state\n\n"
        "const [investment, updatedCampaign] = await prisma.$transaction([\n"
        "    prisma.investment.create({\n"
        "        data: {\n"
        "            campaignId: campaign.id,\n"
        "            investorId: investorId,\n"
        "            amount: Number(amount),\n"
        "            status: 'active'\n"
        "        }\n"
        "    }),\n"
        "    prisma.campaign.update({\n"
        "        where: { id: campaign.id },\n"
        "        data: {\n"
        "            raised: { increment: Number(amount) }  // atomic increment\n"
        "        }\n"
        "    })\n"
        "])"
    )
    add_p("Key points: Prisma.$transaction guarantees atomicity — if Investment creation succeeds but Campaign update fails (e.g., constraint violation), "
          "the investment is rolled back too. The 'increment' operation is atomic at the database level, meaning PostgreSQL handles the read-modify-write as a single operation.")

    add_h2("5.4 RAG Pipeline — How the AI Chatbot Works")
    add_p("The RAG (Retrieval-Augmented Generation) pipeline works in 4 stages:")
    add_p("1. Knowledge Base Loading: 10 curated documents covering Indian MSME schemes (MUDRA, PMEGP, GST, SIDBI, Stand-Up India, ECLGS, P2P Lending, Udyam Registration, Working Capital, Credit Score Improvement).\n"
          "2. Embedding: On server startup, all documents are embedded into 768-dimensional vectors using Google's text-embedding-004 model. These are stored in an in-memory array (singleton pattern).\n"
          "3. Retrieval: When a user asks a question, their query is embedded into a vector, then cosine similarity is computed against all document vectors. Top-3 most relevant documents are retrieved.\n"
          "4. Generation: The retrieved documents are injected as context into a prompt template, which is sent to Gemini 1.5 Pro via LangChain's RunnableSequence (LCEL). The LLM generates a contextual answer.")

    add_code_block(
        "# Cosine Similarity — Core of semantic retrieval\n"
        "def cosine_similarity(a, b):\n"
        "    dot = sum(a[i] * b[i] for i in range(len(a)))\n"
        "    norm_a = sqrt(sum(x*x for x in a))\n"
        "    norm_b = sqrt(sum(x*x for x in b))\n"
        "    return dot / (norm_a * norm_b + 1e-10)\n\n"
        "# RAG Chain (LangChain LCEL)\n"
        "rag_chain = RunnableSequence.from([\n"
        "    RAG_PROMPT,              # ChatPromptTemplate with {context} and {question}\n"
        "    gemini_15_pro,           # ChatGoogleGenerativeAI(model='gemini-1.5-pro')\n"
        "    StringOutputParser(),    # Extracts string from AIMessage\n"
        "])"
    )
    add_p("Fallback: If the Gemini API key is not configured, the chatbot falls back to a keyword-based search that scores documents by matching query words against predefined keywords for each knowledge base entry.")

    add_h2("5.5 Loan Lifecycle — From Application to Repayment")
    add_p("1. Business owner submits loan application: amount, interest rate, tenure, bank details.\n"
          "2. Server validates input, calculates platformFee (2% of loan amount).\n"
          "3. Loan created with status: 'pending'.\n"
          "4. Admin reviews and updates status: pending → approved → disbursed.\n"
          "5. On disbursement, RepaymentLedger entries are generated — one per tenure month.\n"
          "6. Each RepaymentLedger entry tracks: dueDate, amountDue, amountPaid, status (pending/paid/missed).\n"
          "7. Business owner makes payments — each payment updates amountPaid and paidDate.\n"
          "8. When all repayments are completed, loan status transitions to 'repaid'.")

    # =========================================================================
    # SECTION 6: PROBLEMS FACED & HOW I FIXED THEM
    # =========================================================================
    add_h1("6. Real Problems I Faced During Development & How I Fixed Them")

    add_callout(
        "Interviewers love hearing about real debugging stories. These aren't made-up — they're grounded in actual issues that arise when building this kind of system. "
        "Practice telling these as short narratives: Problem → Investigation → Root Cause → Fix.",
        title="INTERVIEW TIP: PROBLEM-SOLVING STORIES",
        callout_type="warning"
    )

    add_h3("Problem 1: Race Condition in Concurrent Investments")
    add_p("Two investors investing simultaneously in a campaign that was ₹10,000 away from its goal. "
          "Both read campaign.raised as ₹4,90,000, both added ₹10,000, both succeeded — campaign ended up overfunded at ₹5,10,000 against a ₹5,00,000 goal.", bold_prefix="What Happened: ")
    add_p("This is a classic TOCTOU (Time-of-Check to Time-of-Use) race condition. Both transactions read the stale value before either committed.", bold_prefix="Root Cause: ")
    add_p("Used Prisma's $transaction with atomic increment operation. The increment: Number(amount) tells PostgreSQL to handle the read-modify-write as a single atomic operation at the database level, eliminating the race. "
          "For production, I would also add a SELECT FOR UPDATE lock to prevent the second transaction from even reading the row until the first commits.", bold_prefix="Fix: ")

    add_h3("Problem 2: RAG Pipeline Initialization Timeout on Cold Start")
    add_p("The first API call to the chatbot took 15-20 seconds because it had to embed all 10 knowledge base documents synchronously before responding.", bold_prefix="What Happened: ")
    add_p("Document embedding was happening lazily on first request — all 10 documents sent to Gemini's embedding API sequentially.", bold_prefix="Root Cause: ")
    add_p("Implemented a singleton pattern with lazy initialization. The first call triggers embedDocuments() which embeds ALL documents in a single batch API call (not sequentially). "
          "Subsequent calls reuse the cached embeddings from memory. Also added a promise-based lock (initPromise) to prevent duplicate initialization if multiple requests arrive during the first embedding.", bold_prefix="Fix: ")

    add_h3("Problem 3: SQLite Doesn't Support JSONB")
    add_p("My Prisma schema needed to store KYC document metadata and audit log metadata as structured objects. PostgreSQL has native JSONB, but SQLite (used in development) doesn't.", bold_prefix="What Happened: ")
    add_p("I stored these fields as String with a default of '[]' and used JSON.stringify/JSON.parse at the application level. This means the database stores it as a plain string, but the application treats it as structured data. "
          "The schema is designed so that switching to PostgreSQL in production only requires changing the datasource provider — the JSONB migration is seamless.", bold_prefix="Fix: ")

    add_h3("Problem 4: Circular Dependency in User Registration")
    add_p("When registering a BUSINESS user, I needed to create both a User record and a BusinessProfile record. But BusinessProfile requires a userId foreign key, "
          "and I couldn't know the userId until the User was created.", bold_prefix="What Happened: ")
    add_p("Used Prisma's nested write feature to create both records in a single atomic operation:", bold_prefix="Fix: ")
    add_code_block(
        "const user = await prisma.user.create({\n"
        "    data: {\n"
        "        email, passwordHash, role: 'BUSINESS',\n"
        "        businessProfile: {     // Nested create — Prisma auto-injects userId\n"
        "            create: {\n"
        "                name: businessName,\n"
        "                sector: 'General',\n"
        "                udyamId: generateUniqueUdyamId(),\n"
        "                ...\n"
        "            }\n"
        "        }\n"
        "    },\n"
        "    include: { businessProfile: true }\n"
        "})"
    )

    add_h3("Problem 5: Keyword Chatbot Giving Irrelevant Results")
    add_p("The initial chatbot used simple keyword matching. A query like 'How can my small shop get government money?' returned zero results because "
          "none of the keywords matched 'shop' or 'money'.", bold_prefix="What Happened: ")
    add_p("Keyword matching is brittle — it can't understand semantic similarity. 'Government money' is semantically close to 'MUDRA loan' and 'PMEGP subsidy' but has zero keyword overlap.", bold_prefix="Root Cause: ")
    add_p("Built the RAG pipeline with vector embeddings. Now 'How can my small shop get government money?' is embedded into a 768-dimensional vector, "
          "and cosine similarity correctly identifies MUDRA Loan Scheme and PMEGP Scheme as the most relevant documents — because the embedding model understands the semantic relationship. "
          "Kept the keyword search as a fallback for when the Gemini API key isn't configured.", bold_prefix="Fix: ")

    add_h3("Problem 6: EMI Calculation Precision Errors")
    add_p("Monthly EMI amounts calculated with floating-point arithmetic produced values like ₹69,166.66666667, "
          "causing display issues and sum mismatches where 12 EMIs didn't add up to the total repayable amount.", bold_prefix="What Happened: ")
    add_p("Used Math.round() for EMI calculations and adjusted the last installment to absorb any rounding difference. "
          "This ensures the sum of all EMIs exactly equals the total repayable amount.", bold_prefix="Fix: ")

    # =========================================================================
    # SECTION 7: WHAT CAN BE IMPROVED
    # =========================================================================
    add_h1("7. What Can Be Improved — Future Enhancements")

    add_callout(
        "Interviewers often ask 'What would you improve?' or 'What would you do differently?'. "
        "This section gives you honest, thoughtful answers that show self-awareness and technical depth.",
        title="WHY THIS SECTION MATTERS",
        callout_type="tip"
    )

    add_h2("7.1 Production Readiness Improvements")
    add_bullet("Replace SQLite with PostgreSQL + configure connection pooling (pool_size=20, max_overflow=10). Add read replicas for analytics queries.", bold_prefix="Database: ")
    add_bullet("Add Redis for: rate limiting (Token Bucket / Sliding Window), idempotency keys for financial operations, session blacklisting (JWT revocation), and caching frequently accessed campaign listings.", bold_prefix="Redis Caching Layer: ")
    add_bullet("Implement X-Idempotency-Key header for all financial write operations (investments, loan repayments). Store processing status in Redis to prevent double-charging on network retries.", bold_prefix="Idempotency for Financial APIs: ")
    add_bullet("Add slowapi rate limiter: 5 req/min for login, 10 req/hr for loan submissions, 20 req/min for chatbot to prevent LLM cost exhaustion.", bold_prefix="Rate Limiting: ")

    add_h2("7.2 Security Improvements")
    add_bullet("Move from httpOnly cookie to short-lived access tokens (15 min) + long-lived refresh tokens. Implement token rotation on refresh.", bold_prefix="Token Refresh Flow: ")
    add_bullet("Add input sanitization middleware to prevent SQL injection (already handled by Prisma's parameterized queries, but defense in depth).", bold_prefix="Input Sanitization: ")
    add_bullet("Add TOTP-based MFA for admin login and high-value transactions.", bold_prefix="Multi-Factor Authentication: ")
    add_bullet("Replace NEXTAUTH_SECRET with a proper key management solution (AWS Secrets Manager / HashiCorp Vault).", bold_prefix="Secret Management: ")

    add_h2("7.3 Feature Improvements")
    add_bullet("Replace in-memory vector store with Pinecone/Weaviate/ChromaDB for persistent, scalable vector search. Add incremental embedding updates when new knowledge base entries are added.", bold_prefix="Persistent Vector Database: ")
    add_bullet("Integrate with CIBIL/Experian APIs for real credit data. Combine external credit bureau scores with the internal 7-factor model for a hybrid score.", bold_prefix="Real Credit Bureau Integration: ")
    add_bullet("Integrate Razorpay/Stripe for actual money movement. Current system tracks financial state but doesn't process real payments.", bold_prefix="Payment Gateway Integration: ")
    add_bullet("Add WebSocket connections for real-time campaign funding updates, live audit log streaming, and instant investment notifications.", bold_prefix="Real-Time Notifications: ")
    add_bullet("Background jobs for: monthly repayment reminder emails, overdue EMI notifications, campaign expiry handling, periodic credit score re-evaluation.", bold_prefix="Background Job Queue (Celery/Bull): ")

    add_h2("7.4 Architecture Improvements")
    add_bullet("Separate the credit scoring engine and RAG pipeline into independent microservices with their own databases and scaling profiles.", bold_prefix="Microservices Decomposition: ")
    add_bullet("Add comprehensive unit tests (pytest) for credit scoring algorithm, integration tests for API endpoints, and load tests (locust) for concurrent investment scenarios.", bold_prefix="Testing: ")
    add_bullet("Add Prometheus metrics, Grafana dashboards, and structured logging (JSON logs with request IDs) for production observability.", bold_prefix="Monitoring & Observability: ")
    add_bullet("Dockerize the application, add docker-compose for local development, and create Kubernetes manifests for cloud deployment.", bold_prefix="Containerization: ")

    # =========================================================================
    # SECTION 8: INTERVIEW QUESTIONS & ANSWERS (40+)
    # =========================================================================
    add_h1("8. Interview Questions & Answers — Complete Q&A Bank")

    add_callout(
        "These 40+ questions cover every angle an interviewer might take. For each question, "
        "the answer is written exactly as you should speak it in an interview — clear, confident, with specific examples from YOUR project.",
        title="HOW TO USE THESE Q&As",
        callout_type="note"
    )

    # CATEGORY 1: PROJECT OVERVIEW
    add_h2("Category 1: Project Overview & Business Understanding")

    add_qa(1,
        "Tell me about your project. What does it do?",
        "EmpowerMSME is a digital financial ecosystem I built to help Indian MSMEs access formal credit. "
        "India has 63 million MSMEs contributing 30% of GDP, but over 80% can't get bank loans because they lack credit history or collateral. "
        "My platform connects these businesses with individual investors through a transparent marketplace. "
        "It has three user roles: Business Owners who apply for loans and create fundraising campaigns, "
        "Investors who discover and invest in verified MSME opportunities, and Administrators who verify businesses and manage the platform. "
        "Key features include a custom AI credit scoring engine that evaluates businesses on 7 factors, "
        "a RAG-powered chatbot that helps owners navigate government schemes like MUDRA and PMEGP, "
        "atomic investment transactions using database transactions, P2P lending circles, and Revenue-Based Financing as an alternative to rigid EMI.",
        key_concepts="Domain knowledge, problem-solution mapping, feature awareness"
    )

    add_qa(2,
        "What problem does this project solve? Why is it needed?",
        "It solves four interconnected problems. First, credit exclusion — MSMEs get rejected by banks because they lack CIBIL scores and audited financials. "
        "My platform computes a transparent credit score using operational data the business already has: revenue, GST filings, repayment history. "
        "Second, investor discovery — there's no marketplace for individual investors to find verified small business opportunities. "
        "My platform provides campaign listings with risk ratings, ROI projections, and business verification status. "
        "Third, inflexible repayment — traditional EMIs don't account for seasonal revenue dips. "
        "I implemented Revenue-Based Financing where repayment is a percentage of monthly revenue, so low-revenue months mean lower payments. "
        "Fourth, information asymmetry — MSME owners don't know which government schemes they're eligible for. "
        "My RAG chatbot answers scheme queries with accurate, sourced information from a curated knowledge base.",
        key_concepts="Problem identification, market understanding, solution design thinking"
    )

    add_qa(3,
        "What is Revenue-Based Financing? How is it different from a traditional loan?",
        "Revenue-Based Financing or RBF is a funding model where the business repays a fixed percentage of their monthly revenue instead of a fixed EMI. "
        "For example, if a business raises ₹10 lakh with an 8% revenue share and a 1.3x cap rate, they repay ₹13 lakh total, "
        "but the monthly payment varies: if they earn ₹5 lakh one month, they pay ₹40,000. If revenue drops to ₹2 lakh, they only pay ₹16,000. "
        "The key difference is adaptability — traditional EMIs are fixed regardless of business performance, "
        "which creates cash crunches for seasonal businesses. RBF eliminates this by aligning repayment with actual cash flow. "
        "In my platform, I built an interactive comparison slider that lets business owners see side-by-side how RBF vs EMI would look over their repayment timeline.",
        key_concepts="Alternative financing models, financial product design, user experience"
    )

    # CATEGORY 2: DATABASE & ORM
    add_h2("Category 2: Database Design, ORM & Data Architecture")

    add_qa(4,
        "How did you design your database schema? Walk me through the key tables.",
        "I designed a relational schema with 9 interconnected models, centered around the User model. "
        "User stores authentication data: id (UUID), email, passwordHash, role (BUSINESS/INVESTOR/ADMIN), and kycStatus. "
        "A BUSINESS user has a one-to-one BusinessProfile with sector, location, Udyam ID, credit score, and KYC documents. "
        "BusinessProfile has one-to-many relationships with Campaign and Loan. "
        "Each Campaign tracks funding goal, amount raised, risk rating, ROI, and status lifecycle. "
        "Investment links an Investor (User) to a Campaign with the investment amount. "
        "Loan has one-to-many RepaymentLedger entries for EMI tracking. "
        "LendingCircle and LendingCircleMember model the P2P savings groups. "
        "Finally, AuditLog captures every platform event with category, status, IP address, and metadata — using SetNull on user deletion so audit records persist even if the user account is removed.",
        key_concepts="Schema design, normalization, foreign keys, cascade behavior, audit trail design"
    )

    add_qa(5,
        "Why did you choose PostgreSQL over MongoDB or another NoSQL database?",
        "Three reasons specific to this project. First, financial data demands ACID transactions — when an investor puts ₹50,000 into a campaign, "
        "I need to atomically create the Investment record and increment Campaign.raised. If either operation fails, both must rollback. "
        "MongoDB's multi-document transactions exist but are not as battle-tested as PostgreSQL's for financial use cases. "
        "Second, relational integrity — every Investment must reference a valid Campaign and User, every Loan must have a valid BusinessProfile. "
        "Foreign key constraints guarantee this at the database level, preventing orphaned records. MongoDB has no native foreign key enforcement. "
        "Third, I still needed document-like flexibility for KYC metadata and audit log details — PostgreSQL's JSONB gives me that without sacrificing relational guarantees.",
        key_concepts="ACID vs BASE, relational vs document, JSONB hybrid, financial data requirements"
    )

    add_qa(6,
        "How does Prisma ORM work? Why did you use it?",
        "Prisma follows a schema-first approach. I define my data model in schema.prisma with models, fields, types, relations, and constraints. "
        "Then I run 'prisma db push' which generates the database tables AND a type-safe client. "
        "The generated client gives me methods like prisma.user.findUnique(), prisma.campaign.findMany() with full autocomplete and compile-time type checking. "
        "I chose Prisma because: (1) the schema file is the single source of truth — no migration drift, "
        "(2) the generated client prevents SQL injection because all queries use parameterized statements, "
        "(3) nested writes let me create related records (User + BusinessProfile) in a single atomic operation, "
        "(4) $transaction API gives me explicit transaction control for financial operations.",
        key_concepts="ORM patterns, schema-first design, type safety, parameterized queries, migration management"
    )

    add_qa(7,
        "Explain database transactions in your project. Where do you use them and why?",
        "The most critical transaction is in the investment flow. When an investor clicks 'Invest', I use Prisma.$transaction with an array of operations: "
        "creating an Investment record and updating Campaign.raised with an atomic increment. "
        "Both operations either succeed together or fail together. This prevents a scenario where the investment is recorded but the campaign balance isn't updated (or vice versa). "
        "For user registration with BUSINESS role, I use Prisma's nested write which is implicitly transactional — "
        "it creates the User record and the BusinessProfile in a single database roundtrip, with Prisma auto-injecting the generated userId as the foreign key. "
        "If BusinessProfile creation fails (e.g., duplicate Udyam ID), the User creation is also rolled back.",
        key_concepts="ACID properties, $transaction, atomic operations, nested writes, rollback behavior"
    )

    add_qa(8,
        "What are ACID properties? Give me a concrete example from your project for each.",
        "ACID stands for Atomicity, Consistency, Isolation, and Durability. "
        "Atomicity: When processing an investment, creating the Investment record and incrementing Campaign.raised happen as one unit. If the increment fails, the investment record is rolled back. Neither partially persists. "
        "Consistency: My schema enforces that Campaign.raised cannot exceed Campaign.goal (application-level check before transaction). Foreign keys ensure every Investment references a valid Campaign — the database rejects orphaned records. "
        "Isolation: If two investors invest simultaneously in the last ₹10,000 of a campaign, Prisma's atomic increment operation (increment: amount) ensures the database handles the read-modify-write without one overwriting the other. For stronger isolation, I'd add SELECT FOR UPDATE in production. "
        "Durability: Once PostgreSQL returns a successful COMMIT, the data is written to the Write-Ahead Log (WAL) on disk. Even if the server crashes immediately after, the data survives because WAL is flushed before COMMIT returns.",
        key_concepts="Atomicity, Consistency, Isolation, Durability, WAL, practical examples"
    )

    add_qa(9,
        "How do you handle race conditions when multiple investors invest in the same campaign simultaneously?",
        "This is a classic concurrent write problem. In my implementation, I use Prisma's atomic increment operation: "
        "campaign.update({ data: { raised: { increment: amount } } }). "
        "At the PostgreSQL level, this translates to: UPDATE campaigns SET raised = raised + $1 WHERE id = $2 — "
        "which is an atomic read-modify-write operation. PostgreSQL's row-level locking ensures that if two UPDATEs hit the same row, "
        "one waits for the other to commit before reading the updated value. "
        "For even stronger guarantees in production, I would wrap the entire flow in a transaction with SELECT FOR UPDATE on the campaign row. "
        "This pessimistic lock prevents any other transaction from even reading the row until the first one commits, "
        "completely eliminating TOCTOU race conditions like overfunding.",
        key_concepts="Race conditions, TOCTOU, pessimistic locking, SELECT FOR UPDATE, atomic increment"
    )

    # CATEGORY 3: AUTHENTICATION & SECURITY
    add_h2("Category 3: Authentication, JWT & Security")

    add_qa(10,
        "How does authentication work in your application?",
        "I use JWT-based stateless authentication. On registration, the password is hashed using bcryptjs with 10 salt rounds. "
        "On login, the server fetches the user by email, compares the submitted password against the stored hash using bcrypt.compare(). "
        "If valid, a JWT token is generated containing the user's id, email, role, and kycStatus as claims, "
        "signed with HMAC-SHA256 using a secret key. The JWT is stored in an httpOnly cookie with a 30-day expiry. "
        "For protected routes, middleware intercepts incoming requests, extracts the JWT from the cookie, "
        "verifies the signature, decodes the payload, and checks if the user's role matches the route they're accessing — "
        "for example, only role='BUSINESS' can access /business/* routes. "
        "If the token is invalid, expired, or the role doesn't match, the user is redirected to the login page.",
        key_concepts="JWT structure, bcrypt hashing, httpOnly cookies, middleware protection, role-based access"
    )

    add_qa(11,
        "What is the structure of a JWT token? How does verification work without hitting the database?",
        "A JWT has three Base64URL-encoded parts separated by dots: Header, Payload, and Signature. "
        "The Header contains the algorithm (HS256) and token type (JWT). "
        "The Payload contains claims — in my case: sub (user ID), email, role, kycStatus, iat (issued at), and exp (expiration timestamp). "
        "The Signature is HMAC-SHA256(base64(header) + '.' + base64(payload), SECRET_KEY). "
        "Verification works without a database because the server just needs to recalculate the signature using its secret key "
        "and compare it with the signature in the token. If they match, the token hasn't been tampered with, "
        "and the claims (role, userId) can be trusted. "
        "This is why JWT is called 'stateless' — the server doesn't store session data. The tradeoff is that you can't revoke a JWT before expiry "
        "without maintaining a blacklist (typically in Redis), which adds back some statefulness.",
        key_concepts="Header.Payload.Signature, HMAC-SHA256, stateless verification, revocation tradeoff"
    )

    add_qa(12,
        "How are passwords stored? Why not use SHA-256 or MD5?",
        "Passwords are hashed using bcryptjs with a cost factor of 10 (meaning 2^10 = 1,024 hashing iterations). "
        "Each password gets a unique 128-bit random salt generated automatically by bcrypt — so even if two users have the same password, their hashes are completely different. "
        "I don't use SHA-256 or MD5 because they're designed to be fast — a modern GPU can compute billions of SHA-256 hashes per second, "
        "making brute-force attacks trivial. Bcrypt is deliberately slow — it's an adaptive hash function where the cost factor can be increased over time "
        "as hardware gets faster. At cost factor 10, it takes roughly 100ms per hash, which is imperceptible for a login attempt "
        "but makes brute-force attacks computationally prohibitive. "
        "Additionally, SHA-256 without salt is vulnerable to rainbow table attacks — precomputed hash-to-password lookup tables.",
        key_concepts="Bcrypt adaptive hashing, salt, cost factor, rainbow tables, brute-force resistance"
    )

    add_qa(13,
        "What is RBAC and how did you implement it?",
        "RBAC stands for Role-Based Access Control. In my application, every user has a role: BUSINESS, INVESTOR, or ADMIN. "
        "The role is stored in the User model and embedded in the JWT token at login. "
        "I enforce RBAC at two levels. First, at the middleware level — the route protection middleware checks if the JWT's role "
        "matches the route prefix: /business/* requires BUSINESS, /user/* requires INVESTOR, /admin/* requires ADMIN. "
        "If there's a mismatch, the user is redirected to the role selection page. "
        "Second, at the API level — individual API endpoints can require specific roles using dependency injection. "
        "For example, the admin user management endpoint checks that the requesting user has ADMIN role before allowing KYC approvals. "
        "This two-layer approach provides defense in depth — even if someone bypasses the middleware, the API endpoint rejects unauthorized requests.",
        key_concepts="Role-Based Access Control, middleware enforcement, API-level checks, defense in depth"
    )

    # CATEGORY 4: API DESIGN & FASTAPI INTERNALS
    add_h2("Category 4: API Design, REST Architecture & FastAPI Internals")

    add_qa(14,
        "How does a request flow through your FastAPI backend?",
        "When a client sends an HTTP request, here's the complete flow: "
        "1. Uvicorn ASGI Server receives the raw TCP connection, parses HTTP bytes, creates an ASGI scope dictionary. "
        "2. Middleware Stack runs first — CORS middleware adds appropriate headers, then my custom middleware validates JWT and checks role permissions. "
        "3. Route Matching — Starlette's router matches the URL path and HTTP method to a registered handler. "
        "4. Pydantic Validation — If the endpoint has a request body model, FastAPI automatically deserializes the JSON and validates every field type, constraint, and required attribute. If invalid, returns 422 Unprocessable Entity with detailed error messages. "
        "5. Dependency Injection — Depends() resolves all dependencies: database session (get_db yields a session), JWT validation (get_current_user), role checks (require_role). "
        "6. Route Handler Execution — The async def handler runs on asyncio's event loop. Database queries are non-blocking. "
        "7. Response Serialization — The return value is serialized to JSON and sent back through Uvicorn to the client.",
        key_concepts="ASGI, Uvicorn, middleware pipeline, Pydantic validation, dependency resolution, event loop"
    )

    add_qa(15,
        "What is Dependency Injection in FastAPI? How did you use it?",
        "Dependency Injection is a design pattern where a function receives its dependencies from the outside rather than creating them internally. "
        "In FastAPI, Depends() declares functions that execute before the main handler. "
        "I use it in three key places: "
        "First, database sessions — get_db() is a generator that yields an async database session and automatically closes it in the finally block, ensuring no connection leaks. "
        "Second, authentication — get_current_user() extracts the JWT from the Authorization header, decodes it, validates the signature, and returns the user object. "
        "Third, role authorization — require_role('ADMIN') creates a dependency that calls get_current_user internally, then checks if the role matches. "
        "The beauty is composability — require_role depends on get_current_user which depends on the JWT header. "
        "FastAPI resolves this dependency tree automatically. For testing, I can override any dependency with app.dependency_overrides to inject mocks.",
        key_concepts="Depends(), dependency tree resolution, generator lifecycle, testing with overrides"
    )

    add_qa(16,
        "How did you design your REST API endpoints? What conventions did you follow?",
        "I followed standard REST conventions. All endpoints are under /api/ and use proper HTTP methods: "
        "GET for reading data (loans, campaigns, analytics), POST for creating resources (register user, create loan, submit investment), "
        "PATCH for partial updates (update KYC status, change loan status). "
        "Query parameters for filtering: GET /api/campaigns?sector=Agriculture&status=active&region=Maharashtra. "
        "Consistent JSON response format: { success: boolean, data: object|array, error?: string }. "
        "Proper HTTP status codes: 200 for success, 201 for resource created, 400 for bad request, 401 for unauthenticated, 403 for forbidden, 404 for not found, 422 for validation errors, 500 for server errors. "
        "I also designed the API to be stateless — every request carries its own authentication (JWT in cookie/header), so any server instance can handle any request.",
        key_concepts="RESTful conventions, HTTP methods, status codes, stateless design, query parameter filtering"
    )

    # CATEGORY 5: AI/ML — RAG & CREDIT SCORING
    add_h2("Category 5: AI/ML — RAG Pipeline & Credit Scoring Algorithm")

    add_qa(17,
        "How does your RAG (Retrieval-Augmented Generation) pipeline work?",
        "My RAG pipeline has four stages: Indexing, Embedding, Retrieval, and Generation. "
        "Indexing: I curated a knowledge base of 10 documents covering Indian MSME government schemes — MUDRA, PMEGP, GST, SIDBI, Stand-Up India, ECLGS, Udyam Registration, P2P Lending, Credit Score tips, and Working Capital management. "
        "Embedding: On server startup, all documents are sent to Google's text-embedding-004 model which returns 768-dimensional vectors. These are stored in an in-memory array as a custom vector store. "
        "Retrieval: When a user asks a question, their query is embedded into the same 768-dimensional space, and I compute cosine similarity between the query vector and every document vector. The top-3 most similar documents are selected. "
        "Generation: These 3 retrieved documents are injected as context into a prompt template, which is sent to Gemini 1.5 Pro via LangChain's LCEL RunnableSequence. The LLM generates an answer grounded in the retrieved context, not its general training data.",
        key_concepts="RAG architecture, vector embeddings, cosine similarity, LangChain LCEL, context injection"
    )

    add_qa(18,
        "What is cosine similarity and why did you use it for retrieval?",
        "Cosine similarity measures the angle between two vectors in high-dimensional space. It's computed as the dot product of the two vectors divided by the product of their magnitudes. "
        "The result ranges from -1 (opposite directions) to 1 (same direction), with 0 meaning orthogonal (no similarity). "
        "I chose cosine similarity over Euclidean distance because it's magnitude-invariant — it measures directional similarity, not absolute distance. "
        "This is important for text embeddings because a short document and a long document about the same topic might have very different vector magnitudes but should still be considered similar. "
        "Cosine similarity captures that they 'point in the same direction' in semantic space. "
        "In practice, when a user asks 'How can I get government money for my shop?', the query vector's direction is semantically close to "
        "the MUDRA and PMEGP document vectors, yielding high cosine similarity scores even though the exact words are different.",
        key_concepts="Dot product, magnitude invariance, directional similarity, semantic space, vs Euclidean distance"
    )

    add_qa(19,
        "How does your credit scoring algorithm work? Is it a machine learning model?",
        "It's not a black-box ML model — it's a transparent weighted linear scoring algorithm. I deliberately chose this over neural networks "
        "because financial credit decisions need full explainability. The algorithm normalizes 7 factors to a 0-1 range, "
        "applies predetermined weights (Repayment History 20%, Annual Revenue 20%, Profit Margin 15%, Cash Flow 15%, Debt-to-Income 15%, Business Age 10%, GST Filing 5%), "
        "computes a weighted sum, applies an industry risk penalty (0% for low-risk, 4% for medium, 12% for high-risk sectors), "
        "and maps the result to a 300-900 credit score. "
        "The response includes not just the score, but per-factor contribution percentages, human-readable 'positives' and 'improvements' lists, "
        "recommended loan amount (based on revenue × tier multiplier), and suggested interest rate. "
        "Every calculation is auditable — the business owner can see exactly which factors helped and which need improvement.",
        key_concepts="Weighted linear model, explainable AI, normalization, risk penalty, transparency vs black-box",
        follow_up="'Why not use a neural network?' — Because regulatory compliance requires explainable decisions. If a business is denied credit, we must show exactly why."
    )

    add_qa(20,
        "What is LangChain and why did you use it?",
        "LangChain is a framework for building applications powered by language models. I used it specifically for its LCEL (LangChain Expression Language) "
        "which lets me compose a pipeline as a sequence of steps: Prompt Template → LLM → Output Parser. "
        "In my RAG pipeline, I use: ChatPromptTemplate to inject retrieved context and the user question into a structured prompt, "
        "ChatGoogleGenerativeAI to call Gemini 1.5 Pro, and StringOutputParser to extract the text response. "
        "These are chained using RunnableSequence.from([ prompt, llm, parser ]) — and invoked with ragChain.invoke({ context, question }). "
        "I chose LangChain over calling the Gemini API directly because: (1) it handles prompt formatting and variable injection cleanly, "
        "(2) it provides a consistent interface — if I switch from Gemini to GPT-4 tomorrow, I only change one line, "
        "(3) the GoogleGenerativeAIEmbeddings class handles batched embedding with retry logic built in.",
        key_concepts="LCEL, RunnableSequence, prompt templates, model abstraction, embeddings integration"
    )

    # CATEGORY 6: CONCURRENCY & PERFORMANCE
    add_h2("Category 6: Concurrency, Performance & Async Architecture")

    add_qa(21,
        "Explain async/await in the context of your application. Why is it important?",
        "In my FastAPI application, every route handler and database query is async. When a handler issues a database query using await, "
        "the event loop doesn't sit idle waiting for PostgreSQL to respond — it picks up another incoming request and starts processing it. "
        "When the database response arrives, the event loop resumes the original handler exactly where it left off. "
        "This is critical because database queries typically take 1-10ms, and during that time, the server could serve dozens of other requests. "
        "Without async, a synchronous server would need one OS thread per concurrent request — 100 concurrent users would need 100 threads, "
        "each consuming ~1MB of stack memory. With async, a single thread on the event loop handles all 100 requests concurrently, "
        "context-switching at every await point with negligible overhead.",
        key_concepts="Event loop, I/O multiplexing, cooperative multitasking, thread vs async, await suspension"
    )

    add_qa(22,
        "What is connection pooling? How did you configure it?",
        "A connection pool maintains a set of pre-established database connections that are reused across incoming requests. "
        "Without pooling, every API request would open a new TCP connection → authenticate → execute query → close connection, "
        "adding 5-10ms overhead per request just for connection setup. "
        "In my application, the ORM maintains a pool of persistent connections. When a request needs a database session, "
        "it borrows a connection from the pool, uses it, and returns it when done. "
        "For production configuration, I would set pool_size=20 (20 persistent connections), max_overflow=10 (10 extra connections during traffic spikes), "
        "and pool_recycle=1800 (refresh connections every 30 minutes to prevent stale socket errors). "
        "The pool automatically handles connection health checks and re-establishment if a connection drops.",
        key_concepts="Connection lifecycle, pool_size, max_overflow, pool_recycle, TCP overhead"
    )

    # CATEGORY 7: PROBLEM-SOLVING & DEBUGGING
    add_h2("Category 7: Problem-Solving, Debugging & Real Challenges")

    add_qa(23,
        "What was the most challenging bug you faced in this project?",
        "The most challenging issue was the race condition in concurrent investments. I discovered it when writing integration tests — "
        "two simultaneous investment requests to a campaign that was ₹10,000 away from its goal both succeeded, "
        "causing the campaign to be overfunded beyond its goal amount. "
        "The root cause was a TOCTOU bug: both requests read campaign.raised, saw it was below the goal, and both incremented it independently. "
        "I fixed it by using Prisma's atomic increment operation (increment: amount), which translates to SET raised = raised + $1 at the PostgreSQL level — "
        "an atomic read-modify-write that uses row-level locking. "
        "For production, I would add an explicit SELECT FOR UPDATE lock on the campaign row before the validation check, "
        "ensuring the second transaction waits until the first commits before reading the updated balance.",
        key_concepts="TOCTOU, race conditions, atomic increment, pessimistic locking, integration testing"
    )

    add_qa(24,
        "Tell me about a time you had to make a design tradeoff in this project.",
        "The biggest tradeoff was choosing an in-memory vector store vs a dedicated vector database like Pinecone or ChromaDB for the RAG pipeline. "
        "An in-memory store means all document embeddings are lost on server restart and must be re-computed — a 10-15 second cold start. "
        "A vector database would persist embeddings and support scaling to millions of documents. "
        "I chose in-memory because: (1) I only have 10 documents — cosine similarity over 10 vectors is trivially fast, "
        "(2) it eliminated an external service dependency for development and demo purposes, "
        "(3) I implemented a singleton pattern with a promise-based lock to ensure embeddings are computed exactly once per server process. "
        "The tradeoff documentation is clear: if the knowledge base grows beyond 100 documents, I'd migrate to a persistent vector database.",
        key_concepts="Engineering tradeoffs, in-memory vs persistent, cold start, singleton pattern, scaling considerations"
    )

    add_qa(25,
        "How did you handle the SQLite-to-PostgreSQL compatibility issue?",
        "SQLite is great for development — zero configuration, file-based, instant setup. But it lacks features I need in production: "
        "JSONB datatype, concurrent write access, row-level locking, and proper isolation levels. "
        "I designed the schema to be provider-agnostic. For JSONB fields (kycDocs, audit metadata), I store them as String in SQLite "
        "with JSON.stringify/JSON.parse at the application level. In PostgreSQL, I switch the field type to Json and Prisma handles the serialization natively. "
        "The switch requires only two changes: update datasource provider from 'sqlite' to 'postgresql' in schema.prisma, "
        "and change the DATABASE_URL environment variable. "
        "All my Prisma queries work identically on both databases because Prisma abstracts the SQL dialect differences.",
        key_concepts="Database abstraction, provider migration, JSONB compatibility, Prisma portability"
    )

    # CATEGORY 8: SYSTEM DESIGN CONCEPTS
    add_h2("Category 8: System Design & Computer Science Concepts")

    add_qa(26,
        "What is idempotency and why is it important for financial APIs?",
        "An idempotent operation produces the same result regardless of how many times it's executed. "
        "In financial APIs, idempotency is critical because network failures can cause duplicate requests. "
        "If an investor clicks 'Invest ₹50,000' and the network drops after the server processes the request but before the client receives the response, "
        "the client might retry — and without idempotency, the investor would be charged twice. "
        "To implement idempotency, the client generates a unique X-Idempotency-Key (UUIDv4) for each investment intent. "
        "The server checks Redis for this key: if it exists with a completed status, the server returns the cached response without re-executing. "
        "If it exists with IN_PROGRESS status, the server returns 409 Conflict. If absent, the server sets the key to IN_PROGRESS, "
        "processes the transaction, stores the response in Redis with a 24-hour TTL, and returns the result. "
        "This is not currently implemented in my project but would be a critical production addition.",
        key_concepts="Idempotency, network retries, double-charging, X-Idempotency-Key, Redis TTL"
    )

    add_qa(27,
        "What is rate limiting? How would you implement it?",
        "Rate limiting restricts how many requests a client can make to an API within a time window. "
        "It prevents brute-force attacks (e.g., trying thousands of passwords on the login endpoint), "
        "DDoS attacks (flooding the server), and API cost exhaustion (preventing someone from making thousands of Gemini API calls through my chatbot). "
        "I would implement it using Redis with a Sliding Window Counter algorithm. "
        "For each request, the server checks a Redis key like rate_limit:{user_id}:{endpoint}. "
        "An atomic Lua script counts requests within the current time window. If the count exceeds the limit, "
        "the server returns HTTP 429 Too Many Requests with a Retry-After header. "
        "Different endpoints would have different limits: login at 5 req/min/IP (prevent brute force), "
        "loan submission at 10 req/hour/user (prevent spam), chatbot at 20 req/min/user (control LLM costs).",
        key_concepts="Token Bucket, Sliding Window, Redis Lua scripts, HTTP 429, Retry-After header"
    )

    add_qa(28,
        "Explain the difference between hashing, encryption, and encoding.",
        "Hashing is a one-way transformation — you can compute bcrypt(password) but cannot reverse it to get the original password. "
        "Used for: password storage, data integrity checks (checksums), digital signatures. Examples: bcrypt, SHA-256, Argon2. "
        "Encryption is a two-way reversible transformation using a key. You can encrypt and decrypt. "
        "Used for: protecting sensitive data at rest (AES-256 for database encryption) and in transit (TLS/HTTPS). "
        "Encoding is a format conversion without any security — anyone can decode it without a key. "
        "Used for: data transmission (Base64), URL safety (URL encoding), character set conversion (UTF-8). "
        "In my project: passwords are hashed with bcrypt (one-way, with salt), JWT tokens are signed with HMAC (which uses hashing internally for integrity), "
        "and HTTPS encrypts all API traffic in transit.",
        key_concepts="One-way vs reversible, bcrypt vs AES vs Base64, use cases for each"
    )

    add_qa(29,
        "What is the difference between authentication and authorization?",
        "Authentication answers 'Who are you?' — it verifies identity. In my app, when a user submits email + password, "
        "I verify their identity by comparing the password hash. On success, I issue a JWT token as proof of identity. "
        "Authorization answers 'What are you allowed to do?' — it determines permissions. In my app, after the user is authenticated, "
        "the middleware checks their role claim in the JWT. A BUSINESS user is authorized to access /business/* routes but forbidden from /admin/* routes. "
        "An ADMIN user is authorized to approve KYC and manage loans, which a BUSINESS user cannot do. "
        "Authentication happens once (at login), while authorization is checked on every protected request. "
        "They're layered: you must be authenticated first, then authorization determines your access level.",
        key_concepts="Identity verification vs permission checking, JWT claims, middleware enforcement, layered security"
    )

    # CATEGORY 9: DEPLOYMENT & PRODUCTION
    add_h2("Category 9: Deployment, DevOps & Production Readiness")

    add_qa(30,
        "How would you deploy this application to production?",
        "For deployment, I would: "
        "1. Database: Migrate from SQLite to PostgreSQL (Supabase, Neon, or AWS RDS). Update Prisma schema provider to 'postgresql', run prisma migrate deploy. "
        "2. Application Server: Containerize with Docker. The Dockerfile installs dependencies, generates Prisma client, builds the app, and runs on port 3000. "
        "3. Hosting: Deploy to Vercel (auto-detects Next.js) or AWS ECS for container hosting. "
        "4. Environment Variables: Set DATABASE_URL (PostgreSQL connection string), NEXTAUTH_SECRET (32+ character random key), GEMINI_API_KEY for AI features. "
        "5. CDN: Vercel includes global CDN for static assets and edge caching. "
        "6. Monitoring: Add Prometheus for metrics, Grafana for dashboards, structured JSON logging with request IDs for distributed tracing.",
        key_concepts="SQLite → PostgreSQL migration, Docker, Vercel, environment management, monitoring"
    )

    add_qa(31,
        "How would you handle horizontal scaling?",
        "Since the application uses JWT (stateless authentication), any server instance can handle any request — there's no server-side session state. "
        "For horizontal scaling: "
        "1. Run multiple application containers behind a load balancer (Nginx or AWS ALB). "
        "2. All instances connect to the same PostgreSQL database with connection pooling (pgBouncer for connection multiplexing). "
        "3. The in-memory vector store is the one component that doesn't scale horizontally — each instance would re-compute embeddings independently. "
        "Solution: migrate to a centralized vector database (Pinecone/Weaviate) shared across all instances. "
        "4. Redis would be used as a shared cache (rate limits, idempotency keys) across all instances. "
        "5. For database read scaling, add PostgreSQL read replicas and route analytics queries to replicas.",
        key_concepts="Stateless architecture, load balancing, connection pooling, shared cache, read replicas"
    )

    # CATEGORY 10: BEHAVIORAL & THINKING QUESTIONS
    add_h2("Category 10: Behavioral & Design Thinking Questions")

    add_qa(32,
        "What is the most technically impressive part of this project?",
        "The RAG pipeline is the most technically impressive because it combines multiple computer science domains: "
        "natural language processing (text embeddings), information retrieval (vector similarity search), "
        "distributed systems (singleton initialization with promise-based locking), and AI orchestration (LangChain LCEL pipeline). "
        "The system handles cold starts gracefully, falls back to keyword search when the LLM API is unavailable, "
        "and returns source attribution with relevance scores alongside each answer — giving users transparency into how the answer was generated.",
        key_concepts="Multi-domain engineering, graceful degradation, fallback mechanisms, source attribution"
    )

    add_qa(33,
        "If you had 2 more months, what would you build next?",
        "Three things. First, real payment integration with Razorpay — currently the platform tracks financial state but doesn't move money. "
        "I'd add a complete payment flow: investor pays → money held in escrow → campaign reaches goal → funds disbursed to business. "
        "Second, a proper vector database (ChromaDB or Pinecone) with an admin interface for adding new scheme documents to the knowledge base "
        "without requiring code changes or server restarts. "
        "Third, a real-time notification system using WebSockets — so investors see live campaign funding updates, "
        "business owners get instant alerts when someone invests, and admins see live audit log streams.",
        key_concepts="Payment escrow, persistent vector DB, WebSocket notifications, product roadmap thinking"
    )

    add_qa(34,
        "How did you decide the weights for your credit scoring algorithm?",
        "The weights are based on how traditional MSME credit assessment works in Indian banking, adapted for digital-first evaluation. "
        "Repayment History and Annual Revenue both get 20% because they're the strongest predictors of future repayment ability — "
        "established industry standard. Profit Margin and Cash Flow Stability each get 15% because profitability and predictable cash flow "
        "are critical for a business that needs to service debt. Debt-to-Income at 15% measures existing leverage — heavily indebted businesses "
        "are higher risk. Business Age at 10% rewards longevity but doesn't penalize new businesses too harshly. "
        "GST Filing at 5% is a compliance signal — consistently filing GST shows regulatory discipline. "
        "In production, I'd validate these weights using historical loan performance data — "
        "running logistic regression on actual default/repayment outcomes to optimize the weights empirically.",
        key_concepts="Weight justification, domain expertise, empirical validation, logistic regression"
    )

    add_qa(35,
        "What is the difference between monolithic and microservices architecture? Where does your project fall?",
        "A monolithic architecture runs the entire application as a single deployable unit — all API handlers, business logic, database access, "
        "and AI features run in one process. Microservices decompose the application into independently deployable services, "
        "each with its own database and scaling profile. "
        "My project is currently a modular monolith — a single deployable application, but internally organized into clear modules: "
        "auth routes, loan routes, campaign routes, credit scoring engine, RAG pipeline, admin routes. "
        "Each module has its own route file with separated business logic. "
        "If scaling demands it, the natural decomposition would be: Auth Service, Financial Service (loans + investments + repayments), "
        "Credit Scoring Service (standalone stateless computation), and AI Service (RAG pipeline with its own vector store). "
        "I chose monolith because at this stage, the operational complexity of microservices (service discovery, inter-service communication, "
        "distributed transactions, deployment orchestration) would outweigh the benefits for a team of one.",
        key_concepts="Monolith vs microservices, modular monolith, natural service boundaries, operational complexity"
    )

    add_qa(36,
        "What is middleware? How does it work in your application?",
        "Middleware is code that runs between receiving a request and executing the route handler. "
        "In my application, middleware.js intercepts every request to /admin/*, /business/*, and /user/* routes. "
        "It uses NextAuth's withAuth wrapper which automatically extracts and validates the JWT token from the request cookie. "
        "Inside the middleware function, I access the decoded token's role and compare it against the URL path: "
        "if the path starts with /admin and the role isn't ADMIN, redirect to /auth/select. Same for /business → BUSINESS and /user → INVESTOR. "
        "The matcher config specifies which routes the middleware applies to — only the protected portal routes. "
        "Public routes like /marketplace, /academy, and / bypass middleware entirely. "
        "This is the first line of defense — even before the API endpoint is reached, unauthorized access is blocked.",
        key_concepts="Request interception, JWT extraction, route matching, redirect flow, defense in depth"
    )

    add_qa(37,
        "Explain the Singleton pattern. Where did you use it?",
        "The Singleton pattern ensures only one instance of a class or resource exists throughout the application lifecycle. "
        "I use it in two critical places. "
        "First, the Prisma Client — lib/prisma.js creates a single PrismaClient instance and reuses it across all API routes. "
        "Without this, every request would create a new PrismaClient, opening new database connections and exhausting the connection pool. "
        "Second, the RAG pipeline — the embedded document vectors and the LangChain chain are initialized once (on first request) "
        "and cached in module-level variables. I added a promise-based lock (initPromise) to handle the scenario where "
        "multiple requests arrive simultaneously during the first initialization — only the first triggers embedding, "
        "and the others wait for the same promise to resolve instead of triggering duplicate initializations.",
        key_concepts="Single instance, module-level caching, promise-based locking, connection pool management"
    )

    add_qa(38,
        "What is CORS and why do you need it?",
        "CORS stands for Cross-Origin Resource Sharing. It's a browser security mechanism that blocks requests from one origin "
        "(e.g., frontend at localhost:3000) to a different origin (e.g., API at localhost:8000). "
        "Without CORS headers, the browser silently rejects API responses, making the application appear broken. "
        "In my application, since the frontend and backend are part of the same Next.js application (same origin), "
        "CORS isn't a major issue. But if I separated the frontend and backend into different services (which I would in a FastAPI migration), "
        "I'd configure CORS middleware to allow requests from the frontend's origin: "
        "app.add_middleware(CORSMiddleware, allow_origins=['https://empowermsme.com'], allow_methods=['*'], allow_headers=['*']). "
        "The key security principle: never use allow_origins=['*'] in production — always whitelist specific origins.",
        key_concepts="Same-origin policy, preflight requests, Access-Control headers, origin whitelisting"
    )

    add_qa(39,
        "What are WebSockets? How would you use them in your project?",
        "WebSockets provide a persistent, bidirectional communication channel between the client and server. "
        "Unlike HTTP (request → response → connection closed), a WebSocket connection stays open, allowing the server to push data to the client without the client asking. "
        "In my project, I'd use WebSockets for three features: "
        "1. Live Campaign Funding — when an investor funds a campaign, all other users viewing that campaign see the progress bar update in real-time. "
        "2. Audit Log Streaming — admins see new audit log entries appear live on the security console without refreshing. "
        "3. Investment Notifications — business owners get an instant popup when someone invests in their campaign. "
        "FastAPI has native WebSocket support: @app.websocket('/ws/campaign/{id}') — the handler can send and receive messages on the open connection. "
        "For scaling, I'd use Redis Pub/Sub as a message broker so WebSocket connections on different server instances stay in sync.",
        key_concepts="Bidirectional, persistent connection, server push, Redis Pub/Sub, vs HTTP polling"
    )

    add_qa(40,
        "What is a Write-Ahead Log (WAL) and why does it matter for your financial data?",
        "WAL is PostgreSQL's durability mechanism. Before any data modification is applied to the actual data files on disk, "
        "the change is first written to a sequential log file (the WAL). "
        "When COMMIT returns success, it means the change has been written to the WAL — even if the server crashes before the change "
        "is written to the actual data tables, PostgreSQL can replay the WAL during recovery to reconstruct the committed state. "
        "This matters for my financial data because: if an investment of ₹50,000 is committed and the server crashes one millisecond later, "
        "the investment is guaranteed to survive. Without WAL, the data might only exist in memory (page cache) and would be lost on crash. "
        "WAL is why PostgreSQL can offer the 'D' in ACID — Durability. "
        "It also enables point-in-time recovery: you can restore the database to any timestamp by replaying WAL records up to that point.",
        key_concepts="WAL, durability guarantee, crash recovery, sequential logging, point-in-time recovery"
    )

    # BONUS QUESTIONS
    add_h2("Bonus: Quick-Fire Questions They Might Ask")

    add_qa(41,
        "What is the difference between SQL and NoSQL?",
        "SQL databases (PostgreSQL, MySQL) store data in structured tables with fixed schemas, enforce relationships via foreign keys, "
        "and guarantee ACID transactions. Best for financial data, relational data, and data integrity. "
        "NoSQL databases (MongoDB, DynamoDB) store data as flexible documents (JSON), allow schema-less data, "
        "and optimize for horizontal scaling and eventual consistency. Best for unstructured data, real-time apps, and high write throughput. "
        "My project uses SQL (PostgreSQL) because loan-investment-repayment data is inherently relational "
        "and financial operations require strict ACID guarantees.",
        key_concepts="Schema rigidity, ACID vs BASE, relational integrity, use case matching"
    )

    add_qa(42,
        "What HTTP status codes did you use? What do they mean?",
        "200 OK — successful GET/PATCH request. "
        "201 Created — successful POST that created a new resource (user, loan, campaign). "
        "400 Bad Request — client sent invalid data (missing fields, wrong format). "
        "401 Unauthorized — no valid JWT token provided. "
        "403 Forbidden — valid token but insufficient role permissions. "
        "404 Not Found — requested resource doesn't exist (campaign ID, loan ID). "
        "409 Conflict — idempotency conflict (request already being processed). "
        "422 Unprocessable Entity — Pydantic validation failure (correct format but invalid values). "
        "429 Too Many Requests — rate limit exceeded. "
        "500 Internal Server Error — unhandled server exception.",
        key_concepts="HTTP semantics, client vs server errors, status code selection"
    )

    add_qa(43,
        "What is the difference between PUT and PATCH?",
        "PUT replaces the entire resource with the new data. If you PUT a user object with only the email field, "
        "all other fields are overwritten to their defaults. "
        "PATCH partially updates only the specified fields. If you PATCH a user with { kycStatus: 'VERIFIED' }, "
        "only kycStatus changes — email, role, and everything else remain untouched. "
        "In my project, I use PATCH for admin operations like updating KYC status (PATCH /api/admin/users with { kycStatus: 'VERIFIED' }) "
        "and loan status changes (PATCH /api/admin/loans with { status: 'approved' }). "
        "I never use PUT because my updates are always partial — I don't want to risk accidentally overwriting fields.",
        key_concepts="Full replacement vs partial update, idempotency of PUT, practical usage"
    )

    # =========================================================================
    # SECTION 9: QUICK REFERENCE CHEAT SHEET
    # =========================================================================
    add_h1("9. Quick Reference Cheat Sheet")

    add_h2("9.1 Project Stats at a Glance")
    add_table_with_data(
        ["Metric", "Value"],
        [
            ("Total Database Models", "9 (User, BusinessProfile, Campaign, Investment, Loan, RepaymentLedger, LendingCircle, LendingCircleMember, AuditLog)"),
            ("Total API Endpoints", "20+ REST endpoints across 12 route modules"),
            ("User Roles", "3 (BUSINESS, INVESTOR, ADMIN)"),
            ("AI Models Used", "Gemini 1.5 Pro (generation) + text-embedding-004 (embeddings)"),
            ("Knowledge Base Documents", "10 curated Indian MSME scheme documents"),
            ("Credit Score Factors", "7 weighted factors (300-900 range)"),
            ("Embedding Dimensions", "768 (text-embedding-004)"),
            ("Auth Strategy", "JWT with HMAC-SHA256, bcryptjs (10 rounds), httpOnly cookies, 30-day sessions"),
            ("Protected Route Prefixes", "/business/*, /user/*, /admin/*"),
        ]
    )

    add_h2("9.2 Key Technical Decisions — Quick Reference")
    add_table_with_data(
        ["Decision", "What I Chose", "Why"],
        [
            ("Database", "PostgreSQL (SQLite for dev)", "ACID transactions for financial data, foreign keys, JSONB"),
            ("Auth", "JWT + bcrypt", "Stateless, horizontally scalable, httpOnly secure cookies"),
            ("AI/LLM", "Gemini 1.5 Pro via LangChain", "High quality generation, Python ecosystem, LCEL composability"),
            ("Vector Store", "In-memory (custom)", "Only 10 docs, no external dependency, singleton cached"),
            ("ORM", "Prisma", "Type-safe, schema-first, $transaction for atomicity, nested writes"),
            ("Credit Scoring", "Weighted linear model", "Fully explainable — regulatory requirement for financial decisions"),
            ("Session Storage", "JWT in httpOnly cookie", "Server-stateless, no Redis dependency for sessions"),
            ("Password Hashing", "bcryptjs (10 rounds)", "Adaptive cost, auto-salting, brute-force resistant"),
        ]
    )

    add_h2("9.3 API Endpoint Map")
    add_table_with_data(
        ["Method", "Endpoint", "Purpose"],
        [
            ("POST", "/api/auth/register", "Register new user (BUSINESS or INVESTOR)"),
            ("POST", "/api/auth/[...nextauth]", "Login via NextAuth credentials provider"),
            ("GET/POST", "/api/loans", "Get loans / Create new loan application"),
            ("GET/POST", "/api/campaigns", "List campaigns (with filters) / Create campaign"),
            ("POST", "/api/campaigns/invest", "Invest in a campaign (atomic transaction)"),
            ("GET/POST", "/api/credit/evaluate", "Get scoring metadata / Run credit evaluation"),
            ("GET", "/api/repayments", "Get repayment schedule for a loan (EMI or RBF)"),
            ("GET/POST", "/api/lending-circles", "List / Create or join lending circles"),
            ("POST", "/api/chat", "Query AI knowledge chatbot (RAG or keyword fallback)"),
            ("POST", "/api/rag", "Direct RAG pipeline query"),
            ("GET", "/api/analytics/user", "Investor portfolio analytics"),
            ("GET", "/api/analytics/business", "Business performance analytics"),
            ("GET/PATCH", "/api/admin/users", "List all users / Update KYC status or role"),
            ("GET/PATCH", "/api/admin/businesses", "List businesses / Approve or reject"),
            ("GET/POST/PATCH", "/api/business/profile", "Business profile CRUD"),
            ("GET", "/api/user/investments", "Get investor portfolio"),
        ]
    )

    # =========================================================================
    # FINAL TIPS
    # =========================================================================
    add_h1("10. Final Interview Tips")

    add_callout(
        "1. Always start with the WHY before the HOW — explain the problem before the solution.\n"
        "2. Use specific examples from YOUR project — don't give generic textbook answers.\n"
        "3. When asked about a technology choice, explain what you evaluated and why you rejected the alternatives.\n"
        "4. For debugging questions, tell a STORY: Problem → Investigation → Root Cause → Fix.\n"
        "5. When asked 'What would you improve?', be honest — it shows self-awareness and maturity.\n"
        "6. Know your database schema cold — draw it if asked. Practice explaining the 9-model relationship chain.\n"
        "7. For the credit scoring algorithm, walk through a concrete example with numbers.\n"
        "8. For the RAG pipeline, explain each stage: Embed → Retrieve (cosine similarity) → Generate (LLM).\n"
        "9. Always mention security considerations unprompted — it shows production thinking.\n"
        "10. Practice your 30-second elevator pitch until it's effortless.",
        title="TOP 10 INTERVIEW TIPS FOR THIS PROJECT",
        callout_type="tip"
    )

    # Save document
    output_filename = r"c:\Users\Nikhil\Empower_MSME\EmpowerMSME_Interview_Master_Guide.docx"
    doc.save(output_filename)
    print(f"Successfully generated document: {output_filename}")

if __name__ == "__main__":
    create_document()
