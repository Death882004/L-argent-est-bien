import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
import io
from PIL import Image

client = TestClient(app)
API_KEY = "XAF_SECURE_KEY_2026"

@pytest.fixture
def mock_vision_service_analyze_bill():
    """Fixture pour mocker la méthode analyze_bill du VisionService."""
    with patch("services.vision_service.VisionService.analyze_bill") as mock_analyze_bill:
        yield mock_analyze_bill

@pytest.fixture
def mock_image_file():
    """Crée un fichier image JPEG en mémoire pour les tests."""
    img = Image.new("RGB", (100, 100), color = 'red')
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="JPEG")
    byte_arr.seek(0)
    return ("test_bill.jpg", byte_arr.getvalue(), "image/jpeg")

def test_analyze_upload_authentic(mock_vision_service_analyze_bill, mock_image_file):
    """
    Teste l'endpoint /analyze/upload avec un billet authentique.
    """
    mock_vision_service_analyze_bill.return_value = ({
        "is_authentic": True,
        "confidence_score": 0.98,
        "verdict": "AUTHENTIQUE",
        "denomination_detected": "10000 XAF",
        "anomalies": [],
        "security_features_checked": ["filigrane"],
        "recommendation": "Billet conforme."
    }, 1200)

    files = {"file": mock_image_file}
    response = client.post(
        "/analyze/upload",
        files=files,
        data={"denomination": "10000"},
        headers={"X-API-Key": API_KEY}
    )
    
    assert response.status_code == 200
    assert response.json()["verdict"] == "AUTHENTIQUE"
    mock_vision_service_analyze_bill.assert_called_once()

def test_analyze_upload_suspect(mock_vision_service_analyze_bill, mock_image_file):
    """
    Teste l'endpoint /analyze/upload avec un billet suspect.
    """
    mock_vision_service_analyze_bill.return_value = ({
        "is_authentic": False,
        "confidence_score": 0.6,
        "verdict": "SUSPECT",
        "denomination_detected": "5000 XAF",
        "anomalies": [
            {
                "type": "FILIGRANE",
                "severity": "MOYENNE",
                "description": "Filigrane manquant ou altéré",
                "location": "Centre",
                "confidence": 0.7
            }
        ],
        "security_features_checked": ["filigrane"],
        "recommendation": "Vérification manuelle requise."
    }, 1500)

    files = {"file": mock_image_file}
    response = client.post(
        "/analyze/upload",
        files=files,
        data={"denomination": "5000"},
        headers={"X-API-Key": API_KEY}
    )
    
    assert response.status_code == 200
    assert response.json()["verdict"] == "SUSPECT"
    assert len(response.json()["anomalies"]) == 1
    mock_vision_service_analyze_bill.assert_called_once()

def test_analyze_upload_invalid_file_format():
    """
    Teste l'upload avec un format de fichier non supporté.
    """
    invalid_file = ("test.txt", b"ceci n'est pas une image", "text/plain")
    files = {"file": invalid_file}
    response = client.post("/analyze/upload", files=files, headers={"X-API-Key": API_KEY})

    assert response.status_code == 400
    assert "Format d'image invalide ou corrompu" in response.json()["detail"]

def test_analyze_upload_file_too_large():
    """
    Teste l'upload avec un fichier trop volumineux.
    """
    # Crée un fichier de 6MB (plus grand que la limite de 5MB)
    large_file_content = b"\x00" * (6 * 1024 * 1024)
    large_file = ("large.jpg", large_file_content, "image/jpeg")
    files = {"file": large_file}
    response = client.post("/analyze/upload", files=files, headers={"X-API-Key": API_KEY})

    assert response.status_code == 413
    assert "Image trop volumineuse" in response.json()["detail"]

def test_analyze_webcam_authentic(mock_vision_service_analyze_bill):
    """
    Teste l'endpoint /analyze/webcam avec un billet authentique.
    """
    mock_vision_service_analyze_bill.return_value = ({
        "is_authentic": True,
        "confidence_score": 0.99,
        "verdict": "AUTHENTIQUE",
        "denomination_detected": "2000 XAF",
        "anomalies": [],
        "security_features_checked": ["filigrane", "hologramme"],
        "recommendation": "Billet authentique."
    }, 800)

    response = client.post(
        "/analyze/webcam",
        json={
            "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
            "denomination": "2000"
        },
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 200
    assert response.json()["verdict"] == "AUTHENTIQUE"
    mock_vision_service_analyze_bill.assert_called_once()

def test_health_check():
    """
    Teste l'endpoint /health.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["anthropic_reachable"] is True
    assert "version" in response.json()
