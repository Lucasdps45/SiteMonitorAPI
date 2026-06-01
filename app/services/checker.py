import time
import httpx
from app.database import SessionLocal
from app import models
from datetime import datetime, timezone

async def health_check(url: str) -> dict:
    try:
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)

        latency_ms = (time.perf_counter() - start) * 1000

        return {
            'url': url,
            'status_code': response.status_code,
            'is_up': response.status_code < 500,
            'latency_ms': round(latency_ms, 2)
        }
    
    except httpx.RequestError as e:
        return {
            'url': url,
            'status_code': None,
            'is_up': False,
            'latency_ms': None,
            'error': str(e)
        }
    
def save_check(target_id: int, result: dict):
    
    db = SessionLocal()
    try:
        check = models.Check(
            target_id = target_id,
            status_code = result['status_code'],
            latencia_ms = result['latency_ms'],
            is_up = result['is_up'],
            checado_em = datetime.now(timezone.utc)
        )
        db.add(check)
        db.commit()
    finally:
        db.close()

async def run_check(target_id: int, url: str):
    result = await health_check(url)
    save_check(target_id, result)
    return result