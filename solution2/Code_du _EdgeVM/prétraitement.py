from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import uvicorn

app = FastAPI()

CLOUD_IP = '34.130.79.172'  # Remplacez par l'adresse IP réelle du Cloud
CLOUD_DECISION_URL = f'http://{CLOUD_IP}:31002/decisionFinale'

class DataPacket(BaseModel):
    zone_indicator: int
    front_distance: float
    details: str
    detected: str
    start_time: float

@app.post("/analyze")
async def analyze(data: List[DataPacket]):
    print(data)
    try:
        # Trouver les valeurs minimales et maximales pertinentes
        min_front_distance = min(packet.front_distance for packet in data)
        max_zone_indicator = max(packet.zone_indicator for packet in data)
        crosswalk = "occupied" if any(packet.details == "occupied" for packet in data) else "empty"
        detected = "light" if any(packet.detected == "light" for packet in data) else "nothing"
        print("==================")
        # Créer un nouveau paquet avec les données filtrées
        filtered_data = {
            "zone_indicator": max_zone_indicator,
            "front_distance": min_front_distance,
            "crosswalk": crosswalk,
            "detected": detected
        }
        print("filtered_data", filtered_data)
        # Envoyer les données filtrées au Cloud pour prise de décision
        response = requests.post(url=CLOUD_DECISION_URL, json=filtered_data)
        if response.status_code == 200:
            cloud_response = response.json()
            return cloud_response
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error with Cloud server: {response.json()}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analyze error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
