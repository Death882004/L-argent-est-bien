import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from models.request_models import WebcamAnalysisRequest
from models.response_models import BillAnalysisResponse, DenominationInfo
from services.image_service import ImageService
from services.vision_service import VisionService
from config import settings
from utils.security import get_api_key
from loguru import logger

router = APIRouter(prefix="/analyze", tags=["Analyse"])

# Initialisation du service vision (global pour réutilisation)
vision_service = VisionService()

@router.post("/upload", response_model=BillAnalysisResponse)
async def analyze_upload(
    file: UploadFile = File(...),
    denomination: str = Form(None),
    api_key: str = Depends(get_api_key)
):
    """
    Analyse d'un billet XAF via l'upload d'un fichier image (JPG, PNG, WEBP).
    """
    logger.info(f"Requête reçue: POST /analyze/upload - Fichier: {file.filename}")
    
    # 1. Validation et traitement de l'image
    img_b64 = await ImageService.validate_and_process(file)
    
    # 2. Analyse via Gemini Vision
    data, duration = await vision_service.analyze_bill(img_b64, denomination)
    
    # 3. Retour du rapport formaté
    return BillAnalysisResponse(
        request_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow(),
        processing_time_ms=duration,
        model_used=settings.MODEL_NAME,
        **data
    )

@router.post("/webcam", response_model=BillAnalysisResponse)
async def analyze_webcam(
    request: WebcamAnalysisRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Analyse d'un billet XAF via une capture webcam encodée en base64.
    """
    logger.info("Requête reçue: POST /analyze/webcam")
    
    # 1. Traitement de l'image base64
    img_b64 = ImageService.process_base64(request.image_base64)
    
    # 2. Analyse via Gemini Vision
    data, duration = await vision_service.analyze_bill(img_b64, request.denomination)
    
    # 3. Retour du rapport formaté
    return BillAnalysisResponse(
        request_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow(),
        processing_time_ms=duration,
        model_used=settings.MODEL_NAME,
        **data
    )

@router.get("/denominations", response_model=list[DenominationInfo])
async def get_denominations():
    """
    Retourne la liste des coupures XAF supportées et leurs caractéristiques de sécurité.
    """
    return [
        DenominationInfo(
            value="10000", color="Violet/Rouge", 
            security_features=["Filigrane portrait", "Bande holographique", "Fil de sécurité fenêtré"]
        ),
        DenominationInfo(
            value="5000", color="Vert", 
            security_features=["Filigrane portrait", "Motif de sécurité", "Bande iridescente"]
        ),
        DenominationInfo(
            value="2000", color="Bleu", 
            security_features=["Filigrane portrait", "Motif de sécurité", "Fil de sécurité"]
        ),
        DenominationInfo(
            value="1000", color="Bleu ciel", 
            security_features=["Filigrane portrait", "Motif de sécurité", "Fil de sécurité"]
        ),
        DenominationInfo(
            value="500", color="Marron/Orange", 
            security_features=["Filigrane portrait", "Motif de sécurité", "Fil de sécurité"]
        )
    ]
