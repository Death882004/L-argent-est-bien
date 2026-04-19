import sys
from loguru import logger

# Configuration du logger Loguru
def setup_logger():
    """Configure un logging structuré vers la console."""
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    return logger

# Export d'une instance de logger configurée
app_logger = setup_logger()
