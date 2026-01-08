"""
Main Application Entry Point.
Initializes FastAPI and defines the routing.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.models import QueryRequest, QueryResponse
from app.services.rag_service import IntelligenceEngine

# Initialize App
app = FastAPI(
    title="PowerGrid Intelligence API",
    description="RAG-enabled Compliance Assistant for Energy Regulations",
    version="1.0.0"
)

# Initialize Service
engine = IntelligenceEngine()


@app.get("/health")
async def health_check():
    """
    Kubernetes/Azure Readiness Probe.
    """
    return {"status": "active", "service": "intelligence-api"}

@app.post("/api/compliance/ask", response_model=QueryResponse)
async def ask_compliance_question(request: QueryRequest):
    """
    Endpoint: /api/compliance/ask
    Accepts a question, queries the LLM with Regulatory Context, and returns the answer.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Delegate to the RAG Engine
    response = engine.ask_llm(request.question)
    
    return response

# Standard boilerplate to run with python main.py (Optional, since we use Uvicorn via Docker)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)