import json
from fastapi import FastAPI, Request, HTTPException, Depends

app = FastAPI()

def get_secret_token():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('auth_token')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error al leer el archivo de configuración.")

async def auth_middleware(request: Request):
    token = request.headers.get('Authorization')
    secret_token = get_secret_token()

    if token != f"Bearer {secret_token}":
        raise HTTPException(status_code=401, detail="No autorizado")

@app.get('/ruta_protegida', dependencies=[Depends(auth_middleware)])
async def ruta_protegida():
    return {'mensaje': 'Acceso concedido a la ruta protegida'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    