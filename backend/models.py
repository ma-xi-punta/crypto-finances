from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"extend_existing": True}  # <- Agrega esta línea
    
    id = Column(Integer, primary_key=True, index=True)
    crypto = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    price_at_purchase = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
