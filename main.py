from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

#http://127.0.0.1:8000 

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# Modelo de Cliente usando Pydantic
class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str

# Crear instancias de Cliente
clientes = [
    Cliente(id=1, nombre="Juan Pérez", telefono="123456789"),
    Cliente(id=2, nombre="Ana Gómez", telefono="987654321"),
    Cliente(id=3, nombre="Luis Fernández", telefono="456789123"),
]

@app.get("/clientes", response_model=List[Cliente])
def obtener_clientes():
    """Devuelve la lista de todos los clientes."""
    return clientes

@app.get("/clientes/{id}", response_model=Cliente)
def obtener_cliente(id: int):
    """Devuelve un cliente específico por ID."""
    for cliente in clientes:
        if cliente.id == id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")