from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logger import logger

# Initialize Settings
settings = get_settings()

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        openapi_url="/openapi.json"
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application

app = create_application()

@app.get("/")
async def health_check():
    """
    Health check endpoint to verify backend is running.
    """
    logger.info("Health check endpoint called")
    return {
        "status": "active",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

# Include the chat router
from app.api.chat import router as chat_router
app.include_router(chat_router, prefix="/api")

