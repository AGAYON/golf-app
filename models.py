from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Tabla de Campos de Golf
class Campo(Base):
    __tablename__ = "campos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    num_hoyos = Column(Integer, nullable=False)
    par_total = Column(Integer, nullable=False)

    hoyos = relationship("Hoyo", back_populates="campo")
    rondas = relationship("Ronda", back_populates="campo")


# Tabla de Hoyos
class Hoyo(Base):
    __tablename__ = "hoyos"

    id = Column(Integer, primary_key=True, index=True)
    campo_id = Column(Integer, ForeignKey("campos.id"))
    numero_hoyo = Column(Integer, nullable=False)
    par = Column(Integer, nullable=False)
    yardas = Column(Integer, nullable=False)

    campo = relationship("Campo", back_populates="hoyos")


# Tabla de Rondas de Golf
class Ronda(Base):
    __tablename__ = "rondas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)  # Relación con el usuario (por ahora un ID directo)
    campo_id = Column(Integer, ForeignKey("campos.id"))
    fecha_inicio = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)  # Se llena cuando se finaliza la ronda
    score_total = Column(Integer, nullable=True)  # Se calcula al final de la ronda

    campo = relationship("Campo", back_populates="rondas")
    hoyos_jugados = relationship("ScoreHoyo", back_populates="ronda")


# Tabla de Registro de Score por Hoyo
class ScoreHoyo(Base):
    __tablename__ = "score_hoyo"

    id = Column(Integer, primary_key=True, index=True)
    ronda_id = Column(Integer, ForeignKey("rondas.id"))
    hoyo_id = Column(Integer, ForeignKey("hoyos.id"))
    score = Column(Integer, nullable=False)  # Golpes totales en este hoyo
    putts = Column(Integer, nullable=False)  # Número de putts
    penalizaciones = Column(String, nullable=True)  # Out of bounds, water hazard, etc.

    ronda = relationship("Ronda", back_populates="hoyos_jugados")
    hoyo = relationship("Hoyo")


# Tabla de Registro de Golpes por Hoyo
class Golpe(Base):
    __tablename__ = "golpes"

    id = Column(Integer, primary_key=True, index=True)
    score_hoyo_id = Column(Integer, ForeignKey("score_hoyo.id"))
    numero_golpe = Column(Integer, nullable=False)  # 1, 2, 3, etc.
    hit_or_miss = Column(Boolean, nullable=False)  # Hit (1) o Miss (0)
    penalizacion = Column(String, nullable=True)  # Si hubo penalización
    comentarios = Column(String, nullable=True)  # Si hay observaciones adicionales

    score_hoyo = relationship("ScoreHoyo", back_populates="golpes")


ScoreHoyo.golpes = relationship("Golpe", back_populates="score_hoyo")
