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

class ServicioService:
    def __init__(self):
        self.servicios = []

    def crear_servicio(self, servicio: Servicio):
        if any(s.id == servicio.id for s in self.servicios):
            raise HTTPException(status_code=400, detail="Servicio con este ID ya existe.")
        self.servicios.append(servicio)

    def obtener_servicios(self) -> List[Servicio]:
        return self.servicios

    def actualizar_servicio(self, id: int, nuevo_servicio: Servicio):
        for i, servicio in enumerate(self.servicios):
            if servicio.id == id:
                self.servicios[i] = nuevo_servicio
                return
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    def eliminar_servicio(self, id: int):
        for i, servicio in enumerate(self.servicios):
            if servicio.id == id:
                del self.servicios[i]
                return
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    def guardar_servicios_json(self, filename='servicios.json'):
        servicios_dict = [servicio.dict() for servicio in self.servicios]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(servicios_dict, f, ensure_ascii=False, indent=4)

# Instancia del servicio
servicio_service = ServicioService()

@app.post("/servicios", response_model=Servicio, status_code=201)
def crear_servicio(servicio: Servicio):
    servicio_service.crear_servicio(servicio)
    servicio_service.guardar_servicios_json()  # Guardar en JSON después de crear
    return servicio

@app.get("/servicios", response_model=List[Servicio])
def obtener_servicios():
    return servicio_service.obtener_servicios()

@app.put("/servicios/{id}", response_model=Servicio)
def actualizar_servicio(id: int, servicio_actualizado: Servicio):
    servicio_service.actualizar_servicio(id, servicio_actualizado)
    servicio_service.guardar_servicios_json()  # Guardar en JSON después de actualizar
    return servicio_actualizado

@app.delete("/servicios/{id}", status_code=204)
def eliminar_servicio(id: int):
    servicio_service.eliminar_servicio(id)
    servicio_service.guardar_servicios_json()  # Guardar en JSON después de eliminar

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)