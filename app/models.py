from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Target(Base):
    __tablename__ = 'targets'

    id          = Column(Integer, primary_key=True)
    url         = Column(String, nullable=False)
    intervalo   = Column(Integer, nullable=False, default=60)
    ativo       = Column(Boolean, nullable=False, default=True)
    criado_em   = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    checks      = relationship('Check', back_populates='target')
    incidents   = relationship('Incident', back_populates='target')

class Check(Base):
    __tablename__ = 'checks'

    id          = Column(Integer, primary_key=True)
    target_id   = Column(Integer, ForeignKey('targets.id', ondelete='CASCADE'))
    status_code = Column(Integer)
    latencia_ms = Column(Integer)
    is_up       = Column(Boolean, nullable=False)
    checado_em  = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    target = relationship('Target', back_populates='checks')


class Incident(Base):
    __tablename__ = 'incidents'

    id          = Column(Integer, primary_key=True)
    target_id   = Column(Integer, ForeignKey('targets.id', ondelete='CASCADE'))
    inicio      = Column(DateTime, nullable=False)
    fim         = Column(DateTime)
    duracao_seg = Column(Integer)

    target = relationship('Target', back_populates='incidents')