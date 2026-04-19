import json
import time
import base64
from google import genai
from google.genai import types
from config import settings
from fastapi import HTTPException
from loguru import logger

class VisionService:
    """Service gérant l'appel à l'API Google Gemini Vision (SDK google-genai v1+)."""

    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY est manquante dans la configuration.")
            raise HTTPException(status_code=500, detail="Configuration API Google manquante")

        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        raw = settings.MODEL_NAME
        self.model_id = raw.replace("models/", "") if raw.startswith("models/") else raw

        self.system_prompt = (
            "Tu es un expert en authentification des billets de banque XAF (Franc CFA BEAC). "
            "Réponds UNIQUEMENT en JSON valide."
        )
        logger.info(f"VisionService initialisé avec le modèle : {self.model_id}")

    async def analyze_bill(self, image_base64: str, denomination: str = None):
        try:
            start_time = time.time()
            prompt_user = f"Analyse ce billet XAF. Denomination déclarée : {denomination if denomination else 'Inconnue'}."
            logger.info(f"Envoi à Gemini ({self.model_id})")

            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]

            image_bytes = base64.b64decode(image_base64)

            contents = [
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                types.Part.from_text(text=prompt_user),
            ]

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    temperature=0.1,
                )
            )

            processing_time = int((time.time() - start_time) * 1000)

            if not response.text:
                raise HTTPException(status_code=500, detail="Gemini n'a renvoyé aucun contenu")

            data = json.loads(response.text)
            logger.info(f"Analyse terminée en {processing_time}ms")
            return data, processing_time

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur Gemini: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur interne Gemini: {str(e)}")

    def check_health(self) -> bool:
        try:
            self.client.models.generate_content(
                model=self.model_id,
                contents="ping",
                config=types.GenerateContentConfig(max_output_tokens=1)
            )
            return True
        except Exception:
            return False