import logging
from fastapi import FastAPI, HTTPException

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Funciones de logging
def log_info(message): 
    logger.info(message)

def log_error(message): 
    logger.error(message)

app = FastAPI()

@app.get("/")
async def root():
    log_info("Acceso a la ruta raíz")
    return {"message": "Hello, World!"}

@app.get("/clientes/{id}")
async def obtener_cliente(id: int):
    log_info(f"Intentando obtener cliente con ID: {id}")
    # Simulando la búsqueda de un cliente
    if id != 1:  # Suponiendo que solo existe un cliente con ID 1
        log_error(f"Cliente con ID {id} no encontrado.")
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    log_info(f"Cliente con ID {id} encontrado.")
    return {"id": id, "nombre": "Juan Pérez", "telefono": "123456789"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)