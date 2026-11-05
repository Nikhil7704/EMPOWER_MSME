import os
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.schemas import ChatRequest, StoryBuilderRequest
from app.services.rag_service import query_rag_pipeline, generate_pitch
from app.core.config import settings

router = APIRouter(tags=["AI Services"])

@router.post("/chat")
def chat_assistant(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")
    
    result = query_rag_pipeline(req.message)
    return {
        "success": True,
        "answer": result["answer"],
        "mode": "rag" if bool(settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")) else "knowledge-base",
        "sources": [{"topic": s, "relevanceScore": 0.95} for s in result.get("sources", [])],
        "model": result.get("model", "FastAPI Python RAG"),
        "pipeline": "FastAPI + LangChain + Google Gemini AI Engine"
    }

@router.get("/rag")
def rag_status():
    has_key = bool(settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"))
    return {
        "service": "EmpowerMSME Agentic RAG Pipeline (FastAPI)",
        "version": "2.0.0",
        "stack": {
            "framework": "FastAPI + LangChain Python",
            "llm": "Google Gemini 1.5 Flash / Pro",
            "embeddingModel": "Google text-embedding-004 (768 dimensions)",
            "vectorStore": "In-Memory Semantic Knowledge Index",
            "retrieval": "Top-K Semantic Similarity Search (k=3)"
        },
        "ready": True,
        "mode": "Full Gemini RAG" if has_key else "Local Knowledge Base Fallback",
        "message": (
            "RAG pipeline is configured and ready for semantic search + generation."
            if has_key
            else "GEMINI_API_KEY not set. Running in fast keyword + semantic fallback mode."
        )
    }

@router.post("/story-builder")
def story_builder(req: StoryBuilderRequest):
    pitches = generate_pitch(req.model_dump())
    return {
        "success": True,
        "data": pitches
    }
