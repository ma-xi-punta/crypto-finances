from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_transaction, get_transactions
from ..services import get_crypto_price
from ..models import Transaction
from pydantic import BaseModel
from typing import List
from ..schemas import TransactionResponse  # Usa el esquema de schemas.py

router = APIRouter()

# Definir esquema Pydantic para la transacción
class TransactionCreate(BaseModel):
    crypto: str
    amount: float

@router.post("/transactions/", response_model=TransactionResponse)
def add_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Agrega una nueva transacción de criptomonedas a la base de datos."""
    price = get_crypto_price(transaction.crypto)
    if price is None:
        raise HTTPException(status_code=400, detail="No se pudo obtener el precio de la criptomoneda.")
    
    return create_transaction(db, transaction.crypto, transaction.amount, price)

@router.get("/transactions/", response_model=List[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    """Lista todas las transacciones registradas en la base de datos."""
    transactions = db.query(Transaction).all()
    return [TransactionResponse.from_orm(tx) for tx in transactions]  # Convirtiendo date a string correctamente


@router.get("/portfolio/")
def get_portfolio(db: Session = Depends(get_db)):
    """Calcula el portafolio actual con el valor actualizado de las criptomonedas."""
    transactions = db.query(Transaction).all()
    portfolio = {}

    for tx in transactions:
        current_price = get_crypto_price(tx.crypto)
        if current_price is not None:
            value = tx.amount * current_price
            if tx.crypto in portfolio:
                portfolio[tx.crypto]['total_value'] += value
                portfolio[tx.crypto]['total_amount'] += tx.amount
            else:
                portfolio[tx.crypto] = {
                    'total_value': value,
                    'total_amount': tx.amount,
                    'current_price': current_price
                }

    return {"portfolio": portfolio}
