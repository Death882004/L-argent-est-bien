import base64
import io
from PIL import Image
from fastapi import HTTPException, UploadFile
from config import settings

class ImageService:
    """Service gérant la validation, le redimensionnement et l'encodage des images."""

    @staticmethod
    async def validate_and_process(file: UploadFile) -> str:
        """
        Valide un fichier uploadé, le redimensionne si nécessaire et retourne une chaîne base64.
        """
        # Vérification de la taille (avant lecture complète pour efficacité)
        content = await file.read()
        if len(content) > settings.MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"Image trop volumineuse (Max {settings.MAX_IMAGE_SIZE_MB} Mo)")

        try:
            image = Image.open(io.BytesIO(content))
            return ImageService._finalize_image(image)
        except Exception:
            raise HTTPException(status_code=400, detail="Format d'image invalide ou corrompu")

    @staticmethod
    def process_base64(base64_str: str) -> str:
        """
        Décode une chaîne base64 et traite l'image.
        """
        try:
            # Nettoyage du préfixe data:image/... si présent
            if "," in base64_str:
                base64_str = base64_str.split(",")[1]
            
            img_data = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(img_data))
            return ImageService._finalize_image(image)
        except Exception:
            raise HTTPException(status_code=400, detail="Format Base64 invalide ou corrompu")

    @staticmethod
    def _finalize_image(image: Image.Image) -> str:
        """
        Redimensionnement (max 1568px) et conversion en base64 pour Claude Vision.
        """
        max_size = 1568
        if max(image.size) > max_size:
            # Utilisation de Resampling.LANCZOS pour une meilleure qualité
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        buffered = io.BytesIO()
        # Conversion en RGB si nécessaire (JPEG ne supporte pas la transparence)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        image.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
