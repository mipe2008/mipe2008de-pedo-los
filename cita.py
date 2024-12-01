import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo Pydantic para Cita
class Cita(BaseModel):
    id: int
    cliente_id: int
    servicio_id: int
    fecha_hora: str  # Puedes usar str o datetime según tus necesidades

# Lista para almacenar citas (en lugar de usar un archivo JSON directamente)
citas = [
    Cita(id=1, cliente_id=1, servicio_id=2, fecha_hora="2024-05-01T10:00:00"),
    Cita(id=2, cliente_id=2, servicio_id=1, fecha_hora="2024-05-02T11:30:00"),
    Cita(id=3, cliente_id=3, servicio_id=3, fecha_hora="2024-05-03T14:15:00"),
]

# Función para guardar citas en un archivo JSON
def guardar_citas():
    citas_dict = [cita.dict() for cita in citas]
    with open('citas.json', 'w', encoding='utf-8') as f:
        json.dump(citas_dict, f, ensure_ascii=False, indent=4)

# Ruta para obtener todas las citas
@app.get("/citas", response_model=List[Cita])
async def obtener_citas():
    return citas

# Ruta para crear una nueva cita
@app.post("/citas", response_model=Cita)
async def crear_cita(cita: Cita):
    if any(c.id == cita.id for c in citas):
        raise HTTPException(status_code=400, detail="Cita con este ID ya existe.")
    
    citas.append(cita)
    guardar_citas()  # Guardar en JSON después de crear
    return cita

# Ruta para obtener una cita por ID
@app.get("/citas/{id}", response_model=Cita)
async def obtener_cita(id: int):
    for cita in citas:
        if cita.id == id:
            return cita
    raise HTTPException(status_code=404, detail="Cita no encontrada")

# Ruta para actualizar una cita por ID
@app.put("/citas/{id}", response_model=Cita)
async def actualizar_cita(id: int, cita_actualizada: Cita):
    for index, cita in enumerate(citas):
        if cita.id == id:
            citas[index] = cita_actualizada
            guardar_citas()  # Guardar en JSON después de actualizar
            return cita_actualizada
    raise HTTPException(status_code=404, detail="Cita no encontrada")

# Ruta para eliminar una cita por ID
@app.delete("/citas/{id}", status_code=204)
async def eliminar_cita(id: int):
    for index, cita in enumerate(citas):
        if cita.id == id:
            del citas[index]
            guardar_citas()  # Guardar en JSON después de eliminar
            return  # No se devuelve nada en caso de éxito
    raise HTTPException(status_code=404, detail="Cita no encontrada")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)