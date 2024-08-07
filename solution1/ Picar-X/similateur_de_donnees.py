import requests
import random
import time

import json

def get_config():
    with open('data.json', 'r') as file:
        return json.load(file)
config = get_config()
db_ip = config[db_ip]
print(cluster_ip)
gateway_url = f"http://{db_ip}:31000/gateway"

while True:
    # Générer des paquets de données aléatoires
    data = []
    for _ in range(100):  # Générer 100 paquets de données
        packet = {
            "zone_indicator": random.randint(200, 400),
            "front_distance": random.uniform(10, 60),
            "details": random.choice(["empty", "occupied"]),
            "detected": random.choice(["nothing", "light"]),
            "start_time": time.time()
        }
        data.append(packet)

    try:
        # Envoi de la requête POST à votre gateway avec tous les paquets de données
        t1 = time.time()
        response = requests.post(url=gateway_url, json=data)
        t2 = time.time()
        response_time = t2 - t1
        print(f"temps de réponse {(response_time) * 1000} ms")
        if response.status_code == 200:
            print("Données envoyées avec succès à la gateway.")
            print("Réponse du serveur gateway:", response.json())
        else:
            print(f"Erreur lors de l'envoi des données à la gateway. Code d'erreur : {response.status_code}")
            print("Détails de l'erreur :", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")

    # Attendre un certain temps avant d'envoyer le prochain lot de données
    time.sleep(1)
