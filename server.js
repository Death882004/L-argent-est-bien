const express = require('express');
const swaggerUi = require('swagger-ui-express');
const app = express();
app.use(express.json());

// --- DONNÉES ---
let etudiants = [
    { id: 1, nom: "Anaella", note: 18, mention: "Excellent", qr_validation: "VALID-99" }
];

// --- LOGIQUE INNOVANTE : Générateur de QR de Validation ---
const genererValidation = (note) => {
    if (note >= 10) return "QR-OK-" + Math.floor(Math.random() * 1000);
    return "QR-ECHEC";
};

// --- ROUTES ---
app.get('/notes', (req, res) => res.json(etudiants));

app.post('/notes', (req, res) => {
    const { nom, note } = req.body;
    const nouvelEtudiant = {
        id: etudiants.length + 1,
        nom,
        note,
        mention: note >= 10 ? "Admis" : "Ajourné",
        qr_validation: genererValidation(note)
    };
    etudiants.push(nouvelEtudiant);
    res.status(201).json(nouvelEtudiant);
});

// --- SPECIFICATION OPENAPI 3 (Le Plan) ---
const swaggerDocument = {
    openapi: "3.0.0",
    info: { 
        title: "API Académique Elitiste", 
        version: "1.0.0",
        description: "Gestion des notes avec validation par QR Code automatique." 
    },
    paths: {
        "/notes": {
            get: { summary: "Récupérer la liste complète" },
            post: {
                summary: "Ajouter un étudiant",
                requestBody: {
                    content: { "application/json": { 
                        schema: { type: "object", properties: { nom: {type: "string"}, note: {type: "number"} } } 
                    } }
                }
            }
        }
    }
};

// Route pour l'interface visuelle
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Route pour le fichier JSON (Pour automatiser Postman)
app.get('/swagger.json', (req, res) => res.json(swaggerDocument));

app.listen(3000, () => {
    console.log("✅ SERVEUR OK sur le port 3000");
    console.log("🔗 Interface Web : http://localhost:3000/docs");
    console.log("📥 Lien Import Postman : http://localhost:3000/swagger.json");
});