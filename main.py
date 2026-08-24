from fastapi import FastAPI

app = FastAPI(title="VeriHire AI API")

@app.get("/")
async def root():
    return {"status": "active", "system": "Dual-Engine Detector Online"}