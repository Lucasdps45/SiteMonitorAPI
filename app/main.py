from fastapi import FastAPI
from app.routers.targets import router as targets_router

app = FastAPI(title="Site Monitor API")

app.include_router(targets_router)

@app.get("/")
def root():
    return {"status": "online"}