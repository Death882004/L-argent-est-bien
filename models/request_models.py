from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class WebcamAnalysisRequest(BaseModel):
    """Modèle de requête pour l'analyse d'images provenant d'une webcam (Base64)."""
    image_base64: str = Field(..., description="Image encodée en Base64 (incluant ou non le préfixe data:image/...)")
    denomination: Optional[str] = Field(None, description="Valeur faciale présumée du billet (ex: 5000)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                "denomination": "10000"
            }
        }
    )
