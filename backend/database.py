from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime

DATABASE_URL = "sqlite:///./crypto.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    crypto = Column(String, index=True)
    amount = Column(Float)
    price_at_purchase = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)

# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# ✅ Agregar esta función para obtener sesiones de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
