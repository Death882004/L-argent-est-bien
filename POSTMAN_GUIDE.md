# Guide d'utilisation de la Collection Postman

Ce guide vous explique comment importer et utiliser la collection Postman fournie pour tester l'API de détection de faux billets XAF.

## 1. Prérequis

*   **Postman Desktop App** : Assurez-vous d'avoir l'application Postman installée sur votre machine. Vous pouvez la télécharger depuis [le site officiel de Postman](https://www.postman.com/downloads/).
*   **API en cours d'exécution** : L'API `fake_bill_detector` doit être lancée et accessible (par exemple, sur `http://localhost:8000`).

## 2. Importation de la Collection

1.  Ouvrez l'application Postman.
2.  Dans le menu supérieur, cliquez sur `File > Import`.
3.  Sélectionnez l'onglet `Files` et cliquez sur `Upload Files`.
4.  Naviguez jusqu'au fichier `postman_collection.json` fourni dans le projet et sélectionnez-le.
5.  Cliquez sur `Import`.

La collection `XAF Fake Bill Detector API` devrait apparaître dans votre sidebar gauche sous l'onglet `Collections`.

## 3. Configuration de l'Environnement

La collection utilise des variables d'environnement pour `base_url` et `api_key`.

1.  Dans Postman, cliquez sur l'icône en forme d'œil (Environments) en haut à droite, puis sur `Add` ou `Manage Environments`.
2.  Créez un nouvel environnement (par exemple, `Local Development`).
3.  Ajoutez les variables suivantes :
    *   `base_url` : `http://localhost:8000` (ou l'adresse où votre API est exécutée)
    *   `api_key` : `XAF_SECURE_KEY_2026` (c'est la clé par défaut configurée dans `config.py` et `.env`)
4.  Enregistrez l'environnement.
5.  Sélectionnez cet environnement dans le sélecteur d'environnement (à côté de l'icône en forme d'œil).

## 4. Test des Endpoints

La collection contient les requêtes suivantes, organisées en dossiers :

### Dossier `Health`

*   **GET - Health Check**
    *   **Description** : Vérifie si l'API est en ligne et si le service Anthropic est accessible.
    *   **Comment tester** : Ouvrez la requête et cliquez sur `Send`. Vous devriez obtenir un statut `200 OK` et une réponse JSON indiquant `"status": "ok"`.

### Dossier `Analyze`

*   **GET - Get Denominations**
    *   **Description** : Récupère la liste des coupures XAF supportées et leurs caractéristiques de sécurité.
    *   **Comment tester** : Ouvrez la requête et cliquez sur `Send`. Vous devriez obtenir un statut `200 OK` et une liste JSON des dénominations.

*   **POST - Analyze Bill - Upload File**
    *   **Description** : Analyse un billet XAF en téléchargeant un fichier image.
    *   **Authentification** : Nécessite la clé API dans le header `X-API-Key`.
    *   **Comment tester** :
        1.  Ouvrez la requête.
        2.  Allez dans l'onglet `Body`, puis sélectionnez `form-data`.
        3.  Pour la clé `file`, changez le type de `Text` à `File` et sélectionnez un fichier image de billet XAF sur votre machine.
        4.  Assurez-vous que la clé `denomination` est définie (par exemple, `10000`).
        5.  Cliquez sur `Send`. Vous devriez obtenir un statut `200 OK` et un rapport d'analyse JSON.

*   **POST - Analyze Bill - Webcam (Base64)**
    *   **Description** : Analyse un billet XAF à partir d'une image encodée en Base64 (simulant une capture webcam).
    *   **Authentification** : Nécessite la clé API dans le header `X-API-Key`.
    *   **Comment tester** :
        1.  Ouvrez la requête.
        2.  Allez dans l'onglet `Body`, puis sélectionnez `raw` et assurez-vous que le type est `JSON`.
        3.  Remplacez la valeur de `image_base64` par une vraie chaîne Base64 d'une image de billet XAF (vous pouvez utiliser un convertisseur en ligne pour cela).
        4.  Assurez-vous que la clé `denomination` est définie (par exemple, `10000`).
        5.  Cliquez sur `Send`. Vous devriez obtenir un statut `200 OK` et un rapport d'analyse JSON.

## 5. Exécution des Tests Automatisés (Optionnel)

Certaines requêtes peuvent inclure des scripts de test Postman pour valider automatiquement les réponses.

1.  Pour exécuter tous les tests d'une collection, cliquez sur les `...` à côté du nom de la collection et sélectionnez `Run collection`.
2.  Le `Collection Runner` s'ouvrira, vous permettant d'exécuter toutes les requêtes séquentiellement et de voir les résultats des tests.

Ce guide devrait vous permettre de prendre en main rapidement l'API avec Postman. N'hésitez pas à explorer les requêtes et à modifier les paramètres pour comprendre le comportement de l'API.
