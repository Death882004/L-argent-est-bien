from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class VerdictEnum(str, Enum):
    """Verdict final de l'analyse d'authenticité."""
    AUTHENTIQUE = "AUTHENTIQUE"
    SUSPECT = "SUSPECT"
    FAUX = "FAUX"
    INDETERMINE = "INDÉTERMINÉ"

class AnomalyType(str, Enum):
    """Types d'anomalies détectables sur les billets XAF."""
    FILIGRANE = "FILIGRANE"
    HOLOGRAMME = "HOLOGRAMME"
    ENCRE_UV = "ENCRE_UV"
    MICROIMPRESSION = "MICROIMPRESSION"
    NUMEROTATION = "NUMÉROTATION"
    COULEUR = "COULEUR"
    TEXTURE = "TEXTURE"
    AUTRE = "AUTRE"

class SeverityEnum(str, Enum):
    """Niveaux de gravité des anomalies détectées."""
    FAIBLE = "FAIBLE"
    MOYENNE = "MOYENNE"
    ELEVEE = "ÉLEVÉE"

class Anomaly(BaseModel):
    """Détails d'une anomalie spécifique détectée."""
    type: AnomalyType
    severity: SeverityEnum
    description: str
    location: str
    confidence: float

class DenominationInfo(BaseModel):
    """Informations sur une coupure XAF supportée."""
    value: str
    color: str
    security_features: List[str]

class BillAnalysisResponse(BaseModel):
    """Réponse détaillée suite à l'analyse d'un billet de banque."""
    request_id: str
    timestamp: datetime
    is_authentic: bool
    confidence_score: float
    verdict: VerdictEnum
    denomination_detected: str
    anomalies: List[Anomaly]
    security_features_checked: List[str]
    recommendation: str
    processing_time_ms: int
    model_used: str
