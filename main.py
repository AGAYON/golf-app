from fastapi import FastAPI
from database import engine
import models

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API de Golf en funcionamiento"}
