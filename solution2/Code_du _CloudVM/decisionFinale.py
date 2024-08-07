from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.post("/decisionFinale")
async def decision(data: dict):
    try:
                # Simulation d'une charge CPU
        for _ in range(1000):  # Le facteur détermine la >
            _ = [x * x for x in range(1000)]  
        instruction = {'action': '', 'trafic': ''}

        dist = data["front_distance"]
        crosswalk = data["crosswalk"]
        light = data["detected"]

        if crosswalk == "empty":
            if dist < 20:
                instruction["action"] = "brake"
            elif dist > 40:
                instruction["action"] = "slow down"
            else:
                instruction["action"] = "keep going"
        else:
            if dist > 50:
                instruction["action"] = "keep going"
            elif dist > 40 and dist <= 50:
                instruction["action"] = "slow down"
            else:
                instruction["action"] = "brake"

        if light == "light":
            instruction["trafic"] = "5s stop"

        return instruction

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decision error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=31002)
