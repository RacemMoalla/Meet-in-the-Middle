from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import uvicorn

app = FastAPI()

EDGE_IP = '7.1.5.150'  # Remplacez par l'adresse IP réelle de l'EdgeVM
EDGE_ANALYZE_URL = f'http://{EDGE_IP}:5000/analyze'

class DataPacket(BaseModel):
    zone_indicator: int
    front_distance: float
    details: str
    detected: str
    start_time: float

@app.post("/forward_to_edge")
async def forward_to_edge(data: List[DataPacket]):
    try:
        # Journaliser les données reçues
        print("Données reçues:", data)
        # Envoyer les données à l'Edge pour analyse
        response = requests.post(url=EDGE_ANALYZE_URL, json=[packet.dict() for packet in data])
        if response.status_code == 200:
            edge_response = response.json()
            return edge_response
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error with Edge server: {response.json()}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forwarding error: {str(e)}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=5001)
