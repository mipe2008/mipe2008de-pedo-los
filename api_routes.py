from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
api_router = APIRouter()

# Definición de modelos Pydantic
class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str

class Cita(BaseModel):
    id: int
    cliente_id: int  # Suponiendo que cada cita tiene un cliente asociado
    fecha: str       # Cambia el tipo según tus necesidades (ej. datetime)
    servicio_id: int

class Servicio(BaseModel):
    id: int
    nombre: str
    precio: float

# Almacenamiento en memoria (puedes cambiar esto por almacenamiento en un archivo o base de datos)
clientes = []
citas = []
servicios = []

# Funciones CRUD para Clientes
@api_router.post("/clientes", response_model=Cliente)
async def crear_cliente(cliente: Cliente):
    if any(c.id == cliente.id for c in clientes):
        raise HTTPException(status_code=400, detail="Cliente con este ID ya existe.")
    
    clientes.append(cliente)
    return cliente

@api_router.get("/clientes", response_model=List[Cliente])
async def obtener_clientes():
    return clientes

@api_router.put("/clientes/{id}", response_model=Cliente)
async def actualizar_cliente(id: int, cliente_actualizado: Cliente):
    for index, cliente in enumerate(clientes):
        if cliente.id == id:
            clientes[index] = cliente_actualizado
            return cliente_actualizado
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@api_router.delete("/clientes/{id}", status_code=204)
async def eliminar_cliente(id: int):
    for index, cliente in enumerate(clientes):
        if cliente.id == id:
            del clientes[index]
            return
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# Funciones CRUD para Citas
@api_router.post("/citas", response_model=Cita)
async def crear_cita(cita: Cita):
    if any(c.id == cita.id for c in citas):
        raise HTTPException(status_code=400, detail="Cita con este ID ya existe.")
    
    citas.append(cita)
    return cita

@api_router.get("/citas", response_model=List[Cita])
async def obtener_citas():
    return citas

@api_router.put("/citas/{id}", response_model=Cita)
async def actualizar_cita(id: int, cita_actualizada: Cita):
    for index, cita in enumerate(citas):
        if cita.id == id:
            citas[index] = cita_actualizada
            return cita_actualizada
    raise HTTPException(status_code=404, detail="Cita no encontrada")

@api_router.delete("/citas/{id}", status_code=204)
async def eliminar_cita(id: int):
    for index, cita in enumerate(citas):
        if cita.id == id:
            del citas[index]
            return
    raise HTTPException(status_code=404, detail="Cita no encontrada")

# Funciones CRUD para Servicios
@api_router.post("/servicios", response_model=Servicio)
async def crear_servicio(servicio: Servicio):
    if any(s.id == servicio.id for s in servicios):
        raise HTTPException(status_code=400, detail="Servicio con este ID ya existe.")
    
    servicios.append(servicio)
    return servicio

@api_router.get("/servicios", response_model=List[Servicio])
async def obtener_servicios():
    return servicios

@api_router.put("/servicios/{id}", response_model=Servicio)
async def actualizar_servicio(id: int, servicio_actualizado: Servicio):
    for index, servicio in enumerate(servicios):
        if servicio.id == id:
            servicios[index] = servicio_actualizado
            return servicio_actualizado
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

@api_router.delete("/servicios/{id}", status_code=204)
async def eliminar_servicio(id: int):
    for index, servicio in enumerate(servicios):
        if servicio.id == id:
            del servicios[index]
            return
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

# Incluir el router en la aplicación principal
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)