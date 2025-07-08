import sqlite3
from getpass import getpass
from colorama import Fore
from db import conectar

def registrar_usuario():
    username = input("Nuevo nombre de usuario: ")
    password = getpass("Contraseña: ")
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
            print(Fore.GREEN + "Usuario registrado correctamente.")
        except sqlite3.IntegrityError:
            print(Fore.RED + "El nombre de usuario ya existe.")

def login():
    intentos = 3
    while intentos > 0:
        username = input("Usuario: ")
        password = getpass("Contraseña: ")
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM usuarios WHERE username = ? AND password = ?", (username, password))
            usuario = cursor.fetchone()
            if usuario:
                print(Fore.GREEN + f"¡Bienvenido/a, {usuario[1]}!")
                return usuario[0]  # retorna el ID del usuario
        intentos -= 1
        print(Fore.RED + f"Credenciales incorrectas. Intentos restantes: {intentos}")
    print(Fore.RED + "Has superado el número máximo de intentos.")
    return None


def cambiar_contraseña():
    username = input("Ingrese su nombre de usuario: ")
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
        usuario = cursor.fetchone()
        if usuario:
            nueva = getpass("Ingrese la nueva contraseña: ")
            confirmar = getpass("Confirme la nueva contraseña: ")
            if nueva != confirmar:
                print(Fore.RED + "Las contraseñas no coinciden.")
                return
            cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (nueva, username))
            conn.commit()
            print(Fore.GREEN + "Contraseña actualizada correctamente.")
        else:
            print(Fore.YELLOW + "El usuario no existe.")

def eliminar_usuario():
    username = input("Ingrese el nombre de usuario a eliminar: ")
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
        if cursor.rowcount > 0:
            conn.commit()
            print(Fore.RED + "Usuario eliminado correctamente.")
        else:
            print(Fore.YELLOW + "El usuario no existe.")
