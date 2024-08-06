import random
from fastapi import FastAPI, HTTPException
import requests
import json
from pydantic import BaseModel 
import time
import uvicorn
import logging
from typing import List, Dict
instruction_count = 0
delay_exceed_count = 0
MAX_DELAY = 0.650
MAX_EXCEED_COUNT = 3
temps_de_reponse: List[float] = []  # Liste pour stocker les temps de réponse
RANDOM_THRESHOLD =50
def get_config():
    with open('data.json', 'r') as file:
        return json.load(file)

def trigger_jenkins_jobs():
    # URL pour le premier job Jenkins
    jenkins_url_1 = "http://34.163.46.231:8080/job/mig-cloud-edge/build"
    # URL pour le deuxième job Jenkins
    jenkins_url_2 = "http://34.163.46.231:8080/job/check%20resources/build"

    # Premier job Jenkins
    response_1 = requests.post(jenkins_url_1, auth=('racem', '1164a3e9d6b45dd19d3f3dedc2bf77444'))
    if response_1.status_code == 201:
        print("Jenkins job 'mig-cloud-edge' triggered successfully.")
    else:
        print(f"Failed to trigger Jenkins job 'mig-cloud-edge': {response_1.status_code}")

    # Deuxième job Jenkins
    response_2 = requests.post(jenkins_url_2, auth=('racem', '1164a3e9d6b45dd19d3f3dedc2bf77444'))
    if response_2.status_code == 201:
        print("Jenkins job 'check resources' triggered successfully.")
    else:
        print(f"Failed to trigger Jenkins job 'check resources': {response_2.status_code}")

app = FastAPI()


class DataPacket(BaseModel):
    zone_indicator: int
    front_distance: float
    details: str
    detected: str
    start_time: float


@app.post("/gateway")
async def decision(data: List[DataPacket]):
    global instruction_count, delay_exceed_count, temps_de_reponse, RANDOM_THRESHOLD
    client_response = {}
    config = get_config()
    cluster_ip = config["cluster_ip"]
    edge_url = f"http://{cluster_ip}/analyze_and_decide"
    apply_delay = config.get("apply_delay", False)

    t1 = time.time()
    edge_response = requests.post(url=edge_url, json= [packet.dict() for packet in data]) 
    # Vérifiez si un délai doit être appliqué(verifier si le service et deployer dans le cloud pour faire une simulation de degradation de latence )
    if apply_delay == "1":
        instruction_count += 1
        # Ajouter un délai aleatoire après RANDOM_THRESHOLD instructions
        if (instruction_count == 1):
            RANDOM_THRESHOLD = random.randint(80, 130)  # Nombre aléatoire entre 80 et 130
            print (RANDOM_THRESHOLD)
        if instruction_count > RANDOM_THRESHOLD :
            RANDOM_TIME = random.uniform(0.3, 0.45)
            time.sleep(RANDOM_TIME)
    else:
        instruction_count = 0
        delay_exceed_count = 0

    t2 = time.time()
    response_time = t2 - t1
    temps_de_reponse.append(response_time * 100)  # Stocker le temps de réponse 
    print(f"temps de réponse {(response_time) * 100} ms")

    if edge_response.status_code == 200:
        instruction = edge_response.json()
        client_response["action"] = instruction["action"]
        client_response["trafic"] = instruction["trafic"]
    else:
        print(f"Something wrong with edge server: Error with {edge_response.status_code}")

    # Vérifiez si le temps de réponse dépasse le délai maximum
    if response_time > MAX_DELAY:
        delay_exceed_count += 1
    else:
        delay_exceed_count = 0

    # Déclencher le job Jenkins si le délai dépasse la limite
    if delay_exceed_count == MAX_EXCEED_COUNT:
        trigger_jenkins_jobs()

    # Écrire les temps de réponse dans un fichier
    with open('delay_log.json', 'w') as file:
        json.dump(temps_de_reponse, file)

    return client_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=31000)
    print("server running")
