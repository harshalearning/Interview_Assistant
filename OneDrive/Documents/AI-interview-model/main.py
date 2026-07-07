from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router as api_router

app = FastAPI(
    title="mock-interview-ai",
    version="0.2.0",
    description="AI-powered interview preparation system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "mock-interview-ai backend is running",
        "version": "0.2.0",
        "endpoints": {
            "health": "/ping",
            "api": "/api/v1",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/ping")
def ping():
    return {"ping": "pong"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }
