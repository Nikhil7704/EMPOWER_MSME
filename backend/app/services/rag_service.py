import os
from typing import Dict, Any, List
from app.core.config import settings

KNOWLEDGE_BASE = [
    {
        "id": "mudra-1",
        "keywords": ["mudra", "pradhan mantri mudra", "pmmy", "shishu", "kishore", "tarun"],
        "topic": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "content": (
            "MUDRA provides collateral-free loans up to ₹10 lakh across 3 tiers: "
            "1. Shishu: Up to ₹50,000 for early stage micro-units. "
            "2. Kishore: ₹50,001 to ₹5 lakh for established businesses needing working capital. "
            "3. Tarun: ₹5 lakh to ₹10 lakh for enterprise expansion. "
            "Interest rates range from 8-12% p.a. through PSU banks, RRBs, and NBFCs. "
            "Requires Aadhaar, PAN, business proof, and 6-month bank statements."
        )
    },
    {
        "id": "pmegp-1",
        "keywords": ["pmegp", "employment generation", "subsidy", "kvic", "khadi"],
        "topic": "Prime Minister Employment Generation Programme (PMEGP)",
        "content": (
            "PMEGP provides credit-linked capital subsidies for micro-enterprises: "
            "General category gets 15% (urban) and 25% (rural) subsidy. "
            "Special categories (SC/ST/OBC/Women/Minorities) receive 25% (urban) and 35% (rural) subsidy. "
            "Project ceilings are ₹50 lakh for manufacturing and ₹20 lakh for service sectors. "
            "Administered by KVIC online at kviconline.gov.in."
        )
    },
    {
        "id": "gst-1",
        "keywords": ["gst", "composition", "turnover", "tax", "gstin"],
        "topic": "GST Compliance & Composition Scheme for MSMEs",
        "content": (
            "Mandatory GST registration threshold is ₹40 lakh annual turnover for goods (₹20 lakh in NE states) "
            "and ₹20 lakh for services. The Composition Scheme allows businesses with turnover up to ₹1.5 Cr "
            "to pay a flat 1% to 5% tax and file quarterly returns (CMP-08) instead of monthly filings."
        )
    },
    {
        "id": "rbf-1",
        "keywords": ["rbf", "revenue-based", "financing", "royalty", "equity-free"],
        "topic": "Revenue-Based Financing (RBF)",
        "content": (
            "RBF provides flexible upfront capital in exchange for a fixed percentage (2-8%) of future monthly gross revenue "
            "until a pre-agreed repayment cap (typically 1.1x to 1.4x) is reached. There are no fixed monthly EMIs; "
            "if sales drop, payments automatically adjust downward, preventing default risks."
        )
    },
    {
        "id": "p2p-circles-1",
        "keywords": ["circle", "chit", "peer-to-peer", "community", "lending circle", "rotation"],
        "topic": "P2P Lending Circles & Community ROSCAs",
        "content": (
            "Lending Circles allow groups of verified MSME peers to contribute fixed monthly amounts to a shared pool. "
            "Each month, one member receives the full lump-sum pool based on lottery or bidding, allowing zero-interest "
            "peer financing while establishing on-chain trust scores for institutional underwriting."
        )
    }
]

def query_rag_pipeline(query: str) -> Dict[str, Any]:
    cleaned_query = query.lower()
    best_match = None
    max_score = 0

    for item in KNOWLEDGE_BASE:
        score = sum(1 for kw in item["keywords"] if kw in cleaned_query)
        if score > max_score:
            max_score = score
            best_match = item

    if not best_match:
        best_match = KNOWLEDGE_BASE[0]

    # If GEMINI_API_KEY is available, we can synthesize with Gemini
    gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import SystemMessage, HumanMessage

            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=gemini_key,
                temperature=0.3
            )
            prompt = (
                f"You are the EmpowerMSME AI Assistant helping Indian MSME owners.\n"
                f"Context from Official Scheme Knowledge Base:\n{best_match['content']}\n\n"
                f"User Question: {query}\n\n"
                f"Provide a helpful, direct, and actionable answer citing practical eligibility and steps."
            )
            response = llm.invoke([HumanMessage(content=prompt)])
            return {
                "answer": response.content,
                "sources": [best_match["topic"]],
                "confidence": 0.95,
                "model": "gemini-1.5-flash + LangChain RAG"
            }
        except Exception:
            pass

    # Keyword fallback
    return {
        "answer": f"**{best_match['topic']}**\n\n{best_match['content']}",
        "sources": [best_match["topic"]],
        "confidence": 0.88,
        "model": "EmpowerMSME Local Semantic Knowledge Base"
    }

def generate_pitch(data: Dict[str, Any]) -> Dict[str, str]:
    name = data.get("businessName", "Our Business")
    sector = data.get("sector", "Enterprise")
    goal = data.get("fundingGoal", 500000)
    rev = data.get("annualRevenue", 2000000)
    purpose = data.get("purpose", "Scaling operations")

    professional = (
        f"**Executive Summary: {name}**\n\n"
        f"Operating in the fast-growing {sector} sector with an established track record and annual turnover of ₹{rev:,.0f}, "
        f"{name} is seeking ₹{goal:,.0f} in growth capital. Capital deployment will focus directly on {purpose}, "
        f"unlocking projected 35% YoY top-line growth with target gross margins exceeding 28%."
    )

    emotional = (
        f"**Our Mission at {name}**\n\n"
        f"We started {name} to solve real problems for our community in the {sector} space. "
        f"Every rupee of the ₹{goal:,.0f} we raise helps us expand local livelihood creation and deliver quality at scale. "
        f"By backing our journey, investors join a purpose-driven mission to build sustainable grassroots prosperity."
    )

    data_driven = (
        f"**Financial Performance & Metrics: {name}**\n\n"
        f"• TTM Revenue: ₹{rev:,.0f}\n"
        f"• Target Funding: ₹{goal:,.0f}\n"
        f"• Use of Proceeds: {purpose}\n"
        f"• Payback Horizon: 18–24 months\n"
        f"• Expected ROI: 14.5% p.a.\n"
        f"• Risk Category: Low-to-Medium based on steady operating cash flow."
    )

    return {
        "professional": professional,
        "emotional": emotional,
        "dataDriven": data_driven
    }
