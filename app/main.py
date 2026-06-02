from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.targets import router as targets_router
from app.services.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(title="Site Monitor API", lifespan=lifespan)

app.include_router(targets_router)

@app.get("/")
def root():
    return {"status": "online"}