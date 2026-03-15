from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.router import router
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Market Analyst AI",
    description="Multi-Agent Stock Market Analyst API",
    version="1.0.0"
)

# CORS config to allow Streamlit UI to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Market Agent FastAPI backend...")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
