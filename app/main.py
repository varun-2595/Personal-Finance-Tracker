from fastapi import FastAPI
from app.core.config import get_settings

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

# Add prefixes to all routes
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Personal Finance Tracker Application!"}