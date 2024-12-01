import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo Pydantic para Cliente
class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str

# Lista para almacenar clientes 
clientes = [
    Cliente(id=1, nombre="Juan Pérez", telefono="123456789"),
    Cliente(id=2, nombre="Ana Gómez", telefono="987654321"),
    Cliente(id=3, nombre="Luis Fernández", telefono="456789123"),
]

# Función para guardar clientes en un archivo JSON
def guardar_clientes():
    clientes_dict = [cliente.dict() for cliente in clientes]
    with open('clientes.json', 'w', encoding='utf-8') as f:
        json.dump(clientes_dict, f, ensure_ascii=False, indent=4)

# Ruta para obtener todos los clientes
@app.get("/clientes", response_model=List[Cliente])
async def obtener_clientes():
    return clientes

# Ruta para crear un nuevo cliente
@app.post("/clientes", response_model=Cliente)
async def crear_cliente(cliente: Cliente):
    # Verificar si el cliente ya existe
    if any(c.id == cliente.id for c in clientes):
        raise HTTPException(status_code=400, detail="Cliente con este ID ya existe.")
    
    clientes.append(cliente)
    guardar_clientes()  # Guardar en JSON después de crear
    return cliente

# Ruta para obtener un cliente por ID
@app.get("/clientes/{id}", response_model=Cliente)
async def obtener_cliente(id: int):
    for cliente in clientes:
        if cliente.id == id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# Ruta para actualizar un cliente por ID
@app.put("/clientes/{id}", response_model=Cliente)
async def actualizar_cliente(id: int, cliente_actualizado: Cliente):
    for index, cliente in enumerate(clientes):
        if cliente.id == id:
            clientes[index] = cliente_actualizado
            guardar_clientes()  # Guardar en JSON después de actualizar
            return cliente_actualizado
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# Ruta para eliminar un cliente por ID
@app.delete("/clientes/{id}", status_code=204)
async def eliminar_cliente(id: int):
    for index, cliente in enumerate(clientes):
        if cliente.id == id:
            del clientes[index]
            guardar_clientes()  # Guardar en JSON después de eliminar
            return  # No se devuelve nada en caso de éxito
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)