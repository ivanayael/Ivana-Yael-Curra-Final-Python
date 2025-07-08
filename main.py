from colorama import init, Fore, Style
import db
import auth
from utils import input_entero, input_float, input_string
from tabulate import tabulate

init(autoreset=True)

def iniciar_aplicacion():
    db.crear_tabla()
    db.crear_tabla_usuarios()

    print(Style.BRIGHT + Fore.BLUE + "\n=== SISTEMA DE INVENTARIO YURU ===")
    print("1. Iniciar sesión")
    print("2. Registrar nuevo usuario")
    print("3. Cambiar contraseña")
    print("4. Eliminar usuario")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        user_id = auth.login()
        if user_id:
            menu(user_id)
    elif opcion == '2':
        auth.registrar_usuario()
        iniciar_aplicacion()
    elif opcion == '3':
        auth.cambiar_contraseña()
        iniciar_aplicacion()
    elif opcion == '4':
        auth.eliminar_usuario()
        iniciar_aplicacion()
    else:
        print(Fore.RED + "Opción inválida.")
        iniciar_aplicacion()

def menu(user_id):
    opciones = {
        '1': lambda: registrar_producto(user_id),
        '2': ver_productos,
        '3': actualizar_producto,
        '4': eliminar_producto,
        '5': buscar_id,
        '6': reporte_stock,
        '7': buscar_por_nombre_o_categoria,
        '8': salir
    }

    while True:
        print(Style.BRIGHT + Fore.BLUE + "\n=== MENÚ INVENTARIO ===")
        print("1. Registrar producto")
        print("2. Ver productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar por ID")
        print("6. Reporte bajo stock")
        print("7. Buscar por nombre o categoría")
        print("8. Salir")
        opcion = input("Opción: ")
        accion = opciones.get(opcion)
        if accion:
            accion()
        else:
            print(Fore.RED + "Opción inválida.")

def registrar_producto(user_id):
    nombre = input_string("Nombre: ")
    descripcion = input_string("Descripción: ")
    cantidad = input_entero("Cantidad: ")
    precio = input_float("Precio: ")
    categoria = input_string("Categoría: ")
    db.agregar_producto(nombre, descripcion, cantidad, precio, categoria, user_id)
    print(Fore.GREEN + f"Producto {nombre} registrado.")

def ver_productos():
    productos = db.obtener_todos()
    if productos:
        for producto_inventariado in productos:
            print(Fore.MAGENTA + "====================================") 
            print("Cantidad de producto en el inventario:  ", len(productos))
            headers = ["Id", "Nombre", "Descripción", "Cantidad", "Precio", "Categoria", "Id de Usuario"]
            data = [producto_inventariado for producto_inventariado in productos]
            tabla = tabulate(data, headers=headers, tablefmt="grid")
            print(tabla)
            print(Fore.MAGENTA + "====================================")    
            print(Style.RESET_ALL)  
    else:
        print(Fore.YELLOW + "No hay productos.")
    

def actualizar_producto():
    id = input_entero("Ingrese el ID a actualizar: ")
    campo = input("Seleccione el campo a actualizar entre estas opciones (nombre, descripcion, cantidad, precio, categoria) y escríbalo a continuación: ").lower()

    if campo == 'cantidad':
        nuevo_valor = input_entero("Nuevo valor de cantidad: ")
    elif campo == 'precio':
        nuevo_valor = input_float("Nuevo valor de precio: ")
    elif campo in ['nombre', 'descripcion', 'categoria']:
        nuevo_valor = input_string(f"Nuevo valor de {campo}: ")
    else:
        print(Fore.RED + "Campo Ingresado no válido.")
        return

    try:
        db.actualizar_producto(id, campo, nuevo_valor)
        print(Fore.GREEN + f"Producto actualizado: {campo} → {nuevo_valor}")
    except ValueError as e:
        print(Fore.RED + str(e))

def eliminar_producto():
    id = input_entero("Ingrese el ID de Producto a eliminar: ")
    db.eliminar_producto(id)
    print(Fore.RED + f"Producto Nro {id} eliminado.")

def buscar_id():
    id = input_entero("Ingrese el ID de Producto a buscar: ")
    resultado = db.buscar_por_id(id)
    if resultado:
        print(Fore.GREEN + "Producto encontrado.")
        print(Fore.MAGENTA + "====================================") 
        headers = ["Id", "Nombre", "Descripción", "Cantidad", "Precio", "Categoria", "Id de Usuario"]
        data = [resultado] # se convierte en una lista de una sola fila
        tabla = tabulate(data, headers=headers, tablefmt="grid") # se usa tabulate para formatear la tabla
        print(tabla)
        print(Fore.MAGENTA + "====================================")    
        print(Style.RESET_ALL)  
    else:
        print(Fore.YELLOW + f"No se encontró el producto nro {id}")

def buscar_por_nombre_o_categoria():
    texto = input_string("Elija buscar por nombre o categoría de: ")
    resultados = db.buscar_nombre_o_categoria(texto)
    if resultados:
        print(Fore.GREEN + f"{len(resultados)} producto(s) encontrado(s).")
        print(Fore.MAGENTA + "====================================")
        headers = ["Id", "Nombre", "Descripción", "Cantidad", "Precio", "Categoria", "Id de Usuario"]
        tabla = tabulate(resultados, headers=headers, tablefmt="grid")
        print(tabla)
        print(Fore.MAGENTA + "====================================")
        print(Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f"No se encontraron coincidencias para '{texto}'.")

def reporte_stock():
    limite = input_entero("Cantidad límite: ")
    resultados = db.productos_bajo_stock(limite)
    if resultados:
        print(Fore.GREEN + "Productos bajo el límite de stock.")
        print(Fore.MAGENTA + "====================================") 
        print("Cantidad de producto bajo el limite de stock:  ", len(resultados))
        headers = ["Id", "Nombre", "Descripción", "Cantidad", "Precio", "Categoria", "Id de Usuario"]
        data = [encontrado for encontrado in resultados]
        tabla = tabulate(data, headers=headers, tablefmt="grid")
        print(tabla)
        print(Fore.MAGENTA + "====================================")    
        print(Style.RESET_ALL)  
    else:
        print(Fore.YELLOW + f"Todos los productos superan el limite de {limite} unidades.")

def salir():
    print(Fore.CYAN + "¡Hasta la próxima vez!")
    exit()

if __name__ == "__main__":
    iniciar_aplicacion()
