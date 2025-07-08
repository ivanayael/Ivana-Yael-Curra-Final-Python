import sqlite3

DB_NAME = "inventario.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT,
                creado_por INTEGER,
                FOREIGN KEY (creado_por) REFERENCES usuarios(id)
            )
        ''')

def crear_tabla_usuarios():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

def agregar_producto(nombre, descripcion, cantidad, precio, categoria, user_id=None):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria, creado_por) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria, user_id)
        )

def obtener_todos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()
    

def actualizar_producto(id, campo, nuevo_valor):
    campos_permitidos = ['nombre', 'descripcion', 'cantidad', 'precio', 'categoria']
    if campo not in campos_permitidos:
        raise ValueError("Campo inválido.")
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE productos SET {campo} = ? WHERE id = ?", (nuevo_valor, id))

def eliminar_producto(id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

def buscar_por_id(id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        return cursor.fetchone()

def buscar_nombre_o_categoria(texto):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM productos 
            WHERE nombre LIKE ? OR categoria LIKE ?
        """, (f"%{texto}%", f"%{texto}%"))
        return cursor.fetchall()

def productos_bajo_stock(limite):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        return cursor.fetchall()
