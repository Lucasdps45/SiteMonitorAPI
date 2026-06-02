import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import SessionLocal
from app import models
from app.services.checker import run_check

scheduler = AsyncIOScheduler()

async def check_all():
    db = SessionLocal()
    try:
        targets = db.query(models.Target).filter(models.Target.ativo == True).all()
    finally:
        db.close()

    tasks = [run_check(t.id, t.url) for t in targets]
    await asyncio.gather(*tasks)

def start_scheduler():
    scheduler.add_job(check_all, 'interval', seconds = 60)
    scheduler.start()