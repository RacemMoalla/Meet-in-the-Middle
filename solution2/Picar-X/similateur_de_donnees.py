import requests
import random
import time

# Endpoint de votre gateway
gateway_url = "http://localhost:5000/gateway"

while True:
    # Générer des paquets de données aléatoires
    data = []
    min= random.uniform(10, 60);
    for _ in range(100):  # Générer 100 paquets de données
        packet = {
            "zone_indicator": random.randint(200, 400),
            "front_distance": random.uniform(min, 60),
            "details": random.choice(["empty", "occupied"]),
            "detected": random.choice(["nothing", "light"]),
            "start_time": time.time()
        }
        data.append(packet)

    try:
        # Envoi de la requête POST à votre gateway avec tous les paquets de données
        response = requests.post(url=gateway_url, json=data)
        if response.status_code == 200:
            print("Données envoyées avec succès à la gateway.")
            print("Réponse du serveur gateway:", response.json())
        else:
            print(f"Erreur lors de l'envoi des données à la gateway. Code d'erreur : {response.status_code}")
            print("Détails de l'erreur :", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")

    # Attendre un certain temps avant d'envoyer le prochain lot de données (par exemple, 1 seconde)
    time.sleep(1)
