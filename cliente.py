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

class ClienteService:
    def __init__(self):
        self.clientes = []

    def crear_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)

    def obtener_clientes(self) -> List[Cliente]:
        return self.clientes

    def actualizar_cliente(self, id: int, nuevo_cliente: Cliente):
        for i, cliente in enumerate(self.clientes):
            if cliente.id == id:
                self.clientes[i] = nuevo_cliente
                return
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    def eliminar_cliente(self, id: int):
        self.clientes = [cliente for cliente in self.clientes if cliente.id != id]

# Crear una instancia del servicio
cliente_service = ClienteService()

# Agregar algunos clientes de ejemplo (puedes quitar esto después)
cliente_service.crear_cliente(Cliente(id=1, nombre="Ailin Martinez", telefono="2604405123"))
cliente_service.crear_cliente(Cliente(id=2, nombre="Ana Gómez", telefono="2604001351"))
cliente_service.crear_cliente(Cliente(id=3, nombre="Luisa Fernández", telefono="2604567891"))

# Ruta para obtener todos los clientes
@app.get("/clientes", response_model=List[Cliente])
async def obtener_clientes():
    return cliente_service.obtener_clientes()

# Ruta para crear un nuevo cliente
@app.post("/clientes", response_model=Cliente)
async def crear_cliente(cliente: Cliente):
    cliente_service.crear_cliente(cliente)
    return cliente

# Ruta para actualizar un cliente por ID
@app.put("/clientes/{id}", response_model=Cliente)
async def actualizar_cliente(id: int, cliente_actualizado: Cliente):
    cliente_service.actualizar_cliente(id, cliente_actualizado)
    return cliente_actualizado

# Ruta para eliminar un cliente por ID
@app.delete("/clientes/{id}", status_code=204)
async def eliminar_cliente(id: int):
    cliente_service.eliminar_cliente(id)

# Función para guardar clientes en un archivo JSON (opcional)
def guardar_clientes():
    clientes_dict = [cliente.dict() for cliente in cliente_service.obtener_clientes()]
    with open('clientes.json', 'w', encoding='utf-8') as f:
        json.dump(clientes_dict, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)