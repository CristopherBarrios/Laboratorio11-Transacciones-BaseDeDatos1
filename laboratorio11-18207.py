import psycopg2



# Establecer conexión con la base de datos
def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="lab11",
        user="postgres",
        password="1234567")
    return conn


# Función 1
def find_pc(velocidad, ram):
    conn = connect()
    cur = conn.cursor()
    cur.execute("BEGIN;")
    cur.execute("SELECT modelo, precio FROM PC WHERE velocidad = %s AND ram = %s;", (velocidad, ram))
    rows = cur.fetchall()
    cur.execute("COMMIT;")
    conn.close()
    if rows:
        for row in rows:
            print("-------------------------------------------------------")
            print("Modelo: %s, Precio: %.2f" % (row[0], row[1]))
            print("-------------------------------------------------------")
    else:
        print("-------------------------------------------------------")
        print("No se encontraron PCs con esa velocidad y RAM.")
        print("-------------------------------------------------------")


# Función 2
def delete_pc(modelo):
    conn = connect()
    cur = conn.cursor()
    cur.execute("BEGIN;")
    cur.execute("DELETE FROM PC WHERE modelo = %s RETURNING modelo;", (modelo,))
    rows = cur.fetchall()
    if rows:
        cur.execute("DELETE FROM Producto WHERE modelo = %s;", (modelo,))
        cur.execute("COMMIT;")
        print("-------------------------------------------------------")
        print("El modelo %s fue eliminado." % rows[0][0])
        print("-------------------------------------------------------")
    else:
        cur.execute("ROLLBACK;")
        print("-------------------------------------------------------")
        print("El modelo %s no existe." % modelo)
        print("-------------------------------------------------------")
    conn.close()


# Función 3
def decrease_price(modelo):
    conn = connect()
    cur = conn.cursor()
    cur.execute("BEGIN;")
    cur.execute("UPDATE PC SET precio = precio - 100.0 WHERE modelo = %s RETURNING modelo;", (modelo,))
    rows = cur.fetchall()
    if rows:
        cur.execute("COMMIT;")
        print("-------------------------------------------------------")
        print("El precio del modelo %s fue decrementado en $100.00." % rows[0][0])
        print("-------------------------------------------------------")
    else:
        cur.execute("ROLLBACK;")
        print("-------------------------------------------------------")
        print("El modelo %s no existe." % modelo)
        print("-------------------------------------------------------")
    conn.close()


# Función 4
def verify_pc(fabricante, modelo, velocidad, ram, disco, precio):
    conn = connect()
    cur = conn.cursor()
    cur.execute("BEGIN;")
    cur.execute("SELECT modelo FROM PC WHERE modelo = %s;", (modelo,))
    rows = cur.fetchall()
    if rows:
        cur.execute("ROLLBACK;")
        print("-------------------------------------------------------")
        print("El modelo %s ya existe." % modelo)
        print("-------------------------------------------------------")
    else:
        cur.execute("INSERT INTO Producto VALUES (%s, %s, %s);", (fabricante, modelo, 'PC'))
        cur.execute("INSERT INTO PC (modelo, velocidad, ram, disco, precio) VALUES (%s, %s, %s, %s, %s);", (modelo, velocidad, ram, disco, precio))
        cur.execute("COMMIT;")
        print("-------------------------------------------------------")
        print("La PC con modelo %s fue agregada exitosamente." % modelo)
        print("-------------------------------------------------------")
    conn.close()

#-------------------------------------------------------------------------------
#-------------------------------Main--------------------------------------------
#-------------------------------------------------------------------------------
while True:
    print("")
    print("")
    print("Seleccione una opción:")
    print("1. Buscar PCs por velocidad y RAM.")
    print("2. Eliminar una PC por modelo.")
    print("3. Decrementar el precio de una PC.")
    print("4. Verificar si una PC existe y agregarla si no.")
    print("5. Salir.")
    print("")
    opcion = input("Ingrese el número de opción: ")
    if opcion == '1':
        velocidad = input("Ingrese la velocidad: ")
        ram = input("Ingrese el tamaño de RAM: ")
        find_pc(velocidad, ram)
    elif opcion == '2':
        modelo = input("Ingrese el modelo: ")
        delete_pc(modelo)
    elif opcion == '3':
        modelo = input("Ingrese el modelo: ")
        decrease_price(modelo)
    elif opcion == '4':
        fabricante = input("Ingrese el fabricante: ")
        modelo = input("Ingrese el modelo: ")
        velocidad = input("Ingrese la velocidad: ")
        ram = input("Ingrese el tamaño de RAM: ")
        disco = input("Ingrese el tamaño de disco duro: ")
        precio = input("Ingrese el precio: ")
        verify_pc(fabricante, modelo, velocidad, ram, disco, precio)
    elif opcion == '5':
        break
    else:
        print("Opción inválida. Intente nuevamente.")
