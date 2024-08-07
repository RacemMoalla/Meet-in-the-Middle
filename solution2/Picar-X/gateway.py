from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import uvicorn
import time
app = FastAPI()

# Adresse IP et ports pour les services sur MVM
MVM_IP = '7.2.5.46'  # Remplacez par l'adresse IP réelle de la MVM
MVM_FORWARD_URL = f'http://{MVM_IP}:5001/forward_to_edge'

class DataPacket(BaseModel):
    zone_indicator: int
    front_distance: float
    details: str
    detected: str
    start_time: float

@app.post("/gateway")
async def gateway(data: List[DataPacket]):
    try:
        t1=time.time()
        # Envoyer toutes les données au MVM pour transmission à l'Edge
        response = requests.post(url=MVM_FORWARD_URL, json=[packet.dict() for packet in data])
        t2=time.time()
        print(f"temps de réponse {(t2-t1)*100} ms")
        if response.status_code == 200:
            mvm_response = response.json()
            return mvm_response
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error with MVM server: {response.json()}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gateway error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
