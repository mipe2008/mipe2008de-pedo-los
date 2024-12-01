API Peluquería
Descripción
Esta es una API para gestionar una peluquería con funcionalidades CRUD.

Requisitos
Python 3.x
json
Instalación
Clona el repositorio.
Crea un entorno virtual:
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
Instala las dependencias:
pip install -r requirements.txt
Ejecución
Ejecuta la aplicación:

python src/controllers/cliente_controller.py 
Descripción de las Carpetas y Archivos
controllers: Contiene la lógica que maneja las solicitudes HTTP. Cada controlador se encarga de un recurso específico.
models: Define las clases que representan los datos en la base de datos, utilizando un ORM como SQLAlchemy.
routes: Aquí se definen las rutas y endpoints que la API expondrá.
services: Contiene la lógica del negocio, interactuando con los modelos y controladores.
middlewares: Incluye funciones intermedias que pueden procesar solicitudes antes de llegar a los controladores, como autenticación.
utils: Funciones auxiliares que pueden ser utilizadas en diferentes partes del proyecto, como configuraciones de logging.
config: Archivos para manejar configuraciones globales y variables de entorno.
tests: Contiene pruebas automatizadas para asegurar que cada parte del código funcione correctamente.
Esta estructura modular facilita el mantenimiento y escalabilidad del proyecto, permitiendo agregar nuevas funcionalidades o modificar las existentes sin afectar otras partes del sistema.
