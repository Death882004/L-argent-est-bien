from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import analyze
from config import settings
from services.vision_service import VisionService
from loguru import logger
import uvicorn
import sys

# Configuration du logging structuré
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

app = FastAPI(
    title=settings.APP_NAME,
    description="API de détection de faux billets Franc CFA (Zone BEAC) via Google Gemini Vision",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(analyze.router)

# Instance vision_service pour le healthcheck
vision_service = VisionService()

@app.get("/health", tags=["Système"])
async def health_check():
    """Vérifie l'état de l'API et la connectivité à Google Gemini."""
    logger.info("Healthcheck demandé")
    
    # On vérifie si la clé API Google est présente
    if not settings.GOOGLE_API_KEY:
        return {
            "status": "warning",
            "version": settings.APP_VERSION,
            "gemini_reachable": False,
            "message": "Clé API Google manquante"
        }
    
    # Tentative de ping vers Gemini
    gemini_reachable = vision_service.check_health()
    
    return {
        "status": "ok" if gemini_reachable else "degraded", 
        "version": settings.APP_VERSION, 
        "gemini_reachable": gemini_reachable
    }

@app.on_event("startup")
async def startup_event():
    """Événements au démarrage de l'application."""
    logger.info(f"Démarrage de {settings.APP_NAME} v{settings.APP_VERSION}")
    # Vérification de la nouvelle clé Google
    if not settings.GOOGLE_API_KEY:
        logger.error("ATTENTION: GOOGLE_API_KEY n'est pas configurée. L'analyse ne fonctionnera pas.")
    else:
        logger.info("Configuration Google API Key détectée avec succès.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)