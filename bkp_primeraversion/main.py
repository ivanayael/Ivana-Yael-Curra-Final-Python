from colorama import init, Fore, Style
import db
from utils import input_entero, input_float

init(autoreset=True)

def menu():
    opciones = {
        '1': registrar_producto,
        '2': ver_productos,
        '3': actualizar_producto,
        '4': eliminar_producto,
        '5': buscar_id,
        '6': reporte_stock,
        '7': buscar_texto,
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

def registrar_producto():
    nombre = input_entero("Nombre: ")
    descripcion = input_entero("Descripción: ")
    cantidad = input_entero("Cantidad: ")
    precio = input_float("Precio: ")
    categoria = input_entero("Categoría: ")
    db.agregar_producto(nombre, descripcion, cantidad, precio, categoria)
    print(Fore.GREEN + "Producto registrado.")

def ver_productos():
    productos = db.obtener_todos()
    if productos:
        for p in productos:
            print(Fore.CYAN + str(p))
    else:
        print(Fore.YELLOW + "No hay productos.")

def actualizar_producto():
    id = input_entero("ID a actualizar: ")
    campo = input("Campo a actualizar (nombre, descripcion, cantidad, precio, categoria): Por favor elija uno ").lower()
    nuevo_valor = input(f"Nuevo valor de {campo}: ")
    if campo == 'cantidad':
        nuevo_valor = int(nuevo_valor)
    elif campo == 'precio':
        nuevo_valor = float(nuevo_valor)
    elif campo == 'nombre' or campo == 'descripcion' or campo == 'categoria':
        nuevo_valor = str(nuevo_valor)
    try:
        db.actualizar_producto(id, campo, nuevo_valor)
        print(Fore.GREEN + f"Producto actualizado a {campo} por {nuevo_valor}.")
    except ValueError as e:
        print(Fore.RED + str(e))

def eliminar_producto():
    id = input_entero("ID de Producto a eliminar: ")
    db.eliminar_producto(id)
    print(Fore.RED + f"Producto Nro {id} eliminado.")

def buscar_id():
    id = input_entero("ID de Producto a buscar: ")
    producto = db.buscar_por_id(id)
    if producto:
        print(Fore.CYAN + str(producto))
    else:
        print(Fore.YELLOW + "No se encontró el producto.")

def buscar_texto():
    texto = input_entero("Buscar por nombre o categoría de: ")
    resultados = db.buscar_nombre_o_categoria(texto)
    if resultados:
        for encontrado in resultados:
            print(Fore.GREEN + "Productos encontrados.")
            print(Fore.CYAN + str(encontrado)) 
    else:
        print(Fore.YELLOW + "No se encontraron coincidencias.")

def reporte_stock():
    limite = input_entero("Cantidad límite: ")
    resultados = db.productos_bajo_stock(limite)
    if resultados:
        for encontrado in resultados:
            print(Fore.GREEN + "Productos bajo el límite de stock.")
            print(Fore.MAGENTA + str(encontrado))
    else:
        print(Fore.YELLOW + "Todos los productos superan ese límite.")

def salir():
    print(Fore.CYAN + "Hasta la próxima.")
    exit()

if __name__ == "__main__":
    db.crear_tabla()
    menu()
