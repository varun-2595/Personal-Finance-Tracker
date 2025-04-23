from fastapi import FastAPI
from app.api import auth
from app.core.config import get_settings
from app.api import auth, transactions, categories, budgets

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

app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Authentication"])

app.include_router(transactions.router, prefix=f"{settings.API_PREFIX}/transactions", tags=["Transactions"])

app.include_router(categories.router, prefix=f"{settings.API_PREFIX}/categories", tags=["Categories"])

app.include_router(budgets.router, prefix=f"{settings.API_PREFIX}/budgets", tags=["Budgets"])