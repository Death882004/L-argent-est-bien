import uuid
from datetime import datetime
from fake_bill_detector.models.response_models import BillAnalysisResponse, Anomaly, AnomalyType, SeverityLevel, Verdict
from fake_bill_detector.utils.logger import app_logger

class ReportService:
    """Service gérant la construction du rapport final BillAnalysisResponse."""

    @staticmethod
    def build_analysis_report(vision_result: dict) -> BillAnalysisResponse:
        """
        Prend le résultat brut de Claude Vision et le transforme en BillAnalysisResponse validé.
        """
        try:
            # Transformation des anomalies brutes en objets Anomaly
            anomalies = []
            for item in vision_result.get("anomalies", []):
                anomalies.append(Anomaly(
                    type=AnomalyType(item.get("type", "AUTRE")),
                    severity=SeverityLevel(item.get("severity", "MOYENNE")),
                    description=item.get("description", "Détail non spécifié"),
                    location=item.get("location", "Non spécifiée"),
                    confidence=item.get("confidence", 0.0)
                ))

            # Construction de la réponse finale
            report = BillAnalysisResponse(
                request_id=uuid.uuid4(),
                timestamp=datetime.now(),
                is_authentic=vision_result.get("is_authentic", False),
                confidence_score=vision_result.get("confidence_score", 0.0),
                verdict=Verdict(vision_result.get("verdict", "INDÉTERMINÉ")),
                denomination_detected=vision_result.get("denomination_detected", "Inconnue"),
                anomalies=anomalies,
                security_features_checked=vision_result.get("security_features_checked", []),
                recommendation=vision_result.get("recommendation", "Contacter les autorités compétentes"),
                processing_time_ms=vision_result.get("processing_time_ms", 0),
                model_used=vision_result.get("model_used", "claude-sonnet-4-6")
            )

            # Log du résultat final pour suivi
            app_logger.info(f"Analyse terminée - Request ID: {report.request_id} - Verdict: {report.verdict} - Confiance: {report.confidence_score}")
            
            return report

        except Exception as e:
            app_logger.error(f"Erreur lors de la construction du rapport final: {str(e)}")
            raise
