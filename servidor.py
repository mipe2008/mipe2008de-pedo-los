import http.server
import socketserver
import json
import fastapi

PORT = 8000

# Almacenamiento de datos en memoria
clientes = []

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/clientes':
            # Devolver la lista de clientes en formato JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(clientes).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/clientes':
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos enviados
            nuevo_cliente = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Agregar el nuevo cliente a la lista
            clientes.append(nuevo_cliente)
            
            # Responder con éxito
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'mensaje': 'Cliente creado', 'cliente': nuevo_cliente}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

# Configuración del servidor
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor corriendo en http://localhost:{PORT}")
    httpd.serve_forever()
    