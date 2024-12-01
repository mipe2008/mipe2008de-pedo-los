import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo Pydantic para Cita
class Cita(BaseModel):
    id: int
    cliente_id: int  # Suponiendo que cada cita tiene un cliente asociado
    servicio_id: int
    fecha_hora: str  # Puedes usar str o datetime según tus necesidades

class CitaService:
    def __init__(self):
        self.citas = []

    def crear_cita(self, cita: Cita):
        if any(c.id == cita.id for c in self.citas):
            raise HTTPException(status_code=400, detail="Cita con este ID ya existe.")
        self.citas.append(cita)

    def obtener_citas(self) -> List[Cita]:
        return self.citas

    def actualizar_cita(self, id: int, nueva_cita: Cita):
        for i, cita in enumerate(self.citas):
            if cita.id == id:
                self.citas[i] = nueva_cita
                return
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    def eliminar_cita(self, id: int):
        for i, cita in enumerate(self.citas):
            if cita.id == id:
                del self.citas[i]
                return
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    def guardar_citas_json(self, filename='citas.json'):
        citas_dict = [cita.dict() for cita in self.citas]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(citas_dict, f, ensure_ascii=False, indent=4)

# Instancia del servicio
cita_service = CitaService()

@app.post("/citas", response_model=Cita, status_code=201)
def crear_cita(cita: Cita):
    cita_service.crear_cita(cita)
    cita_service.guardar_citas_json()  # Guardar en JSON después de crear
    return cita

@app.get("/citas", response_model=List[Cita])
def obtener_citas():
    return cita_service.obtener_citas()

@app.put("/citas/{id}", response_model=Cita)
def actualizar_cita(id: int, nueva_cita: Cita):
    cita_service.actualizar_cita(id, nueva_cita)
    cita_service.guardar_citas_json()  # Guardar en JSON después de actualizar
    return nueva_cita

@app.delete("/citas/{id}", status_code=204)
def eliminar_cita(id: int):
    cita_service.eliminar_cita(id)
    cita_service.guardar_citas_json()  # Guardar en JSON después de eliminar

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)