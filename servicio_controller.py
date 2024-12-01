import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo Pydantic para Servicio
class Servicio(BaseModel):
    id: int
    nombre: str
    precio: float

# Lista para almacenar servicios (en lugar de usar un archivo JSON directamente)
servicios = [
    Servicio(id=1, nombre="Corte de cabello", precio=5000),
    Servicio(id=2, nombre="Tinte", precio=30000),
    Servicio(id=3, nombre="Lavado y secado", precio=10000),
    Servicio(id=4, nombre="Alisado y tratamiento", precio=20000),
]

# Función para guardar servicios en un archivo JSON
def guardar_servicios():
    servicios_dict = [servicio.dict() for servicio in servicios]
    with open('servicios.json', 'w', encoding='utf-8') as f:
        json.dump(servicios_dict, f, ensure_ascii=False, indent=4)

# Ruta para obtener todos los servicios
@app.get("/servicios", response_model=List[Servicio])
async def obtener_servicios():
    return servicios

# Ruta para crear un nuevo servicio
@app.post("/servicios", response_model=Servicio)
async def crear_servicio(servicio: Servicio):
    if any(s.id == servicio.id for s in servicios):
        raise HTTPException(status_code=400, detail="Servicio con este ID ya existe.")
    
    servicios.append(servicio)
    guardar_servicios()  # Guardar en JSON después de crear
    return servicio

# Ruta para obtener un servicio por ID
@app.get("/servicios/{id}", response_model=Servicio)
async def obtener_servicio(id: int):
    for servicio in servicios:
        if servicio.id == id:
            return servicio
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

# Ruta para actualizar un servicio por ID
@app.put("/servicios/{id}", response_model=Servicio)
async def actualizar_servicio(id: int, servicio_actualizado: Servicio):
    for index, servicio in enumerate(servicios):
        if servicio.id == id:
            servicios[index] = servicio_actualizado
            guardar_servicios()  # Guardar en JSON después de actualizar
            return servicio_actualizado
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

# Ruta para eliminar un servicio por ID
@app.delete("/servicios/{id}", status_code=204)
async def eliminar_servicio(id: int):
    for index, servicio in enumerate(servicios):
        if servicio.id == id:
            del servicios[index]
            guardar_servicios()  # Guardar en JSON después de eliminar
            return  # No se devuelve nada en caso de éxito
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)