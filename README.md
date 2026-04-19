# XAF Fake Bill Detector API

Détection intelligente de faux billets Franc CFA (Zone BEAC) utilisant Claude 3.5 Vision.

## Fonctionnalités

- **Analyse d'image**: Soumission d'images via upload de fichier ou base64 (webcam).
- **Détection d'anomalies**: Identification détaillée des signes de falsification (filigrane, hologramme, micro-impressions, etc.).
- **Verdict d'authenticité**: Retourne un score de confiance et un verdict (Authentique, Suspect, Faux, Indéterminé).
- **Informations sur les coupures**: Liste des coupures XAF supportées et leurs caractéristiques de sécurité.
- **Santé de l'API**: Endpoint pour vérifier la connectivité au service Anthropic.

## Architecture du Projet

```
fake_bill_detector/
├── main.py                  # Point d'entrée FastAPI
├── config.py                # Variables d'environnement (clé API, seuils)
├── routes/
│   ├── analyze.py           # Endpoints d'analyse
│   └── health.py            # Healthcheck
├── services/
│   ├── vision_service.py    # Appels à Claude Vision (Anthropic)
│   ├── image_service.py     # Prétraitement images (validation, resize, base64)
│   └── report_service.py    # Construction du rapport d'anomalies
├── models/
│   ├── request_models.py    # Schémas Pydantic pour les requêtes
│   └── response_models.py   # Schémas Pydantic pour les réponses
├── utils/
│   └── logger.py            # Logging structuré
├── tests/
│   ├── test_analyze.py
│   └── test_vision_service.py
├── .env                     # ANTHROPIC_API_KEY, seuils (à configurer)
├── requirements.txt         # Dépendances Python
└── README.md                # Ce fichier
```

## Installation

Suivez ces étapes pour configurer et exécuter l'API en local.

### 1. Cloner le dépôt (si applicable)

```bash
git clone <URL_DU_DEPOT>
cd fake_bill_detector
```

### 2. Créer un environnement virtuel et installer les dépendances

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration de l'API Anthropic

Obtenez votre clé API Anthropic sur [Anthropic Console](https://console.anthropic.com/).

Créez un fichier `.env` à la racine du projet (`fake_bill_detector/.env`) et ajoutez-y votre clé API :

```ini
ANTHROPIC_API_KEY="votre_clé_api_anthropic_ici"
# Autres configurations optionnelles (voir config.py pour les valeurs par défaut)
# MODEL_NAME=claude-3-5-sonnet-20240620
# MAX_IMAGE_SIZE_MB=5
# ANTHROPIC_TIMEOUT_SEC=30
# CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### 4. Exécuter l'application

```bash
python main.py
```

L'API sera disponible à l'adresse `http://localhost:8000`. La documentation interactive Swagger UI est accessible via `http://localhost:8000/docs`.

## Utilisation de l'API (Exemples `curl`)

### 1. Vérifier la santé de l'API

```bash
curl -X GET "http://localhost:8000/health"
```

Exemple de réponse :
```json
{
  "status": "ok",
  "anthropic_reachable": true,
  "version": "1.1.0"
}
```

### 2. Obtenir les dénominations supportées

```bash
curl -X GET "http://localhost:8000/analyze/denominations"
```

Exemple de réponse :
```json
[
  {
    "value": "10000",
    "color": "Violet/Rouge",
    "security_features": [
      "Filigrane portrait",
      "Bande holographique",
      "Fil de sécurité fenêtré"
    ]
  },
  // ... autres dénominations
]
```

### 3. Analyser un billet via upload de fichier

Remplacez `path/to/your/bill.jpg` par le chemin de votre image.

```bash
curl -X POST "http://localhost:8000/analyze/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/bill.jpg;type=image/jpeg" \
     -F "denomination=5000"
```

### 4. Analyser un billet via image Base64 (Webcam)

Remplacez `YOUR_BASE64_IMAGE_STRING` par votre chaîne d'image encodée en Base64.

```bash
curl -X POST "http://localhost:8000/analyze/webcam" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d \'{ "image_base64": "YOUR_BASE64_IMAGE_STRING", "denomination": "10000" }\'
```

Exemple de réponse pour l'analyse (upload ou webcam) :
```json
{
  "request_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "timestamp": "2023-10-27T10:30:00.123456",
  "is_authentic": true,
  "confidence_score": 0.98,
  "verdict": "AUTHENTIQUE",
  "denomination_detected": "5000 XAF",
  "anomalies": [],
  "security_features_checked": [
    "filigrane",
    "fil de sécurité",
    "hologramme",
    "microimpression",
    "numérotation",
    "couleur",
    "texture",
    "encres UV"
  ],
  "recommendation": "Billet authentique. Accepter.",
  "processing_time_ms": 1240,
  "model_used": "claude-3-5-sonnet-20240620"
}
```

## Tests

Pour exécuter les tests unitaires, assurez-vous d'être dans l'environnement virtuel et exécutez :

```bash
pytest
```

## Auteur

Manus AI
