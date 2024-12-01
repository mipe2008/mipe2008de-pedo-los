# Lista de usuarios con sus contraseñas
usuarios = [
    {"usuario": "rebecauvilla@gmail.com", "contrasena": "tu_contrasena"},  # Cambia 'tu_contrasena' por la contraseña real
    {"usuario": "usuario2@example.com", "contrasena": "contrasena2"},
    {"usuario": "usuario3@example.com", "contrasena": "contrasena3"},
]

def iniciar_sesion(usuario, contrasena):
    # Verifica si el usuario y la contraseña son correctos
    for user in usuarios:
        if user["usuario"] == usuario and user["contrasena"] == contrasena:
            return True
    return False

def main():
    print("Bienvenido al sistema de inicio de sesión")
    
    # Solicitar el nombre de usuario y la contraseña
    usuario = input("Introduce tu correo electrónico: ")
    contrasena = input("Introduce tu contraseña: ")
    
    # Verificar las credenciales
    if iniciar_sesion(usuario, contrasena):
        print("Inicio de sesión exitoso. Bienvenido!")
    else:
        print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()