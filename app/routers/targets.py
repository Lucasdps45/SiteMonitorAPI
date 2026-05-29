from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app import models

router = APIRouter(prefix="/targets", tags=["targets"])

class TargetCreate(BaseModel):
    url: str
    intervalo: int = 60

class TargetUpdate(BaseModel):
    ativo: bool

@router.post("/")
def criar_target(payload: TargetCreate, db: Session = Depends(get_db)):
    target = models.Target(url=payload.url, intervalo=payload.intervalo)
    db.add(target)
    db.commit()
    db.refresh(target)
    return target

@router.get("/")
def listar_targets(db: Session = Depends(get_db)):
    return db.query(models.Target).all()

@router.patch("/{id}")
def atualizar_target(id: int, payload: TargetUpdate, db: Session = Depends(get_db)):
    target = db.query(models.Target).filter(models.Target.id == id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target não encontrado")
    target.ativo = payload.ativo
    db.commit()
    db.refresh(target)
    return target

@router.delete("/{id}")
def deletar_target(id: int, db: Session = Depends(get_db)):
    target = db.query(models.Target).filter(models.Target.id == id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target não encontrado")
    db.delete(target)
    db.commit()
    return {"message": "Target deletado com sucesso"}