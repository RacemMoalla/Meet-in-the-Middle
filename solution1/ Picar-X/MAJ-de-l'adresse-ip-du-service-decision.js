const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

// Route POST pour recevoir les mises à jour d'adresse IP
app.post('/update-cluster-ip', (req, res) => {
    const updatedIP = req.body.updatedIP;
    const applyDelay = req.body.apply_delay; // Ajouter cette ligne pour récupérer apply_delay

    console.log(`Received updated IP: ${updatedIP}`);
    console.log(`Received apply_delay: ${applyDelay}`); // Afficher la valeur de apply_delay

    // Charger le contenu actuel du fichier data.json
    let data = JSON.parse(fs.readFileSync('data.json'));

    // Mettre à jour l'adresse IP du cluster
    data.cluster_ip = updatedIP;

    // Mettre à jour apply_delay
    if (applyDelay !== undefined) {
        data.apply_delay = applyDelay;
    }

    // Enregistrer les modifications dans data.json
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2));

    console.log('data.json updated successfully');

    // Répondre à la requête avec un statut 200
    res.status(200).send('Address updated successfully');
});

// Démarrer le serveur sur le port spécifié
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
