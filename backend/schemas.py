from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime

class TransactionCreate(BaseModel):
    crypto: str
    amount: float

class TransactionResponse(BaseModel):
    id: int
    crypto: str
    amount: float
    price_at_purchase: float
    date: datetime  # Usa datetime correctamente

    model_config = ConfigDict(from_attributes=True)  # Configuración para Pydantic v2

    @field_serializer("date")
    def serialize_date(self, value: datetime, _info):
        return value.isoformat()  # Devuelve string en formato ISO8601

