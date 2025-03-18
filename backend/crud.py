
import datetime
from sqlalchemy.orm import Session
from .models import Transaction

def create_transaction(db: Session, crypto: str, amount: float, price: float):
    new_transaction = Transaction(
        crypto=crypto,
        amount=amount,
        price_at_purchase=price
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    print("💾 Transacción guardada:", new_transaction.__dict__)  # 🔍 Agregamos un print para depuración
    return new_transaction

def get_transactions(db: Session):
    transactions = db.query(Transaction).all()
    print("📋 Transacciones en la base de datos:", transactions)  # 🔍 Depuración
    return transactions
