from fastapi import FastAPI
from .database import Base, engine
from .api.endpoints import router

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API de criptomonedas en funcionamiento 🚀"}