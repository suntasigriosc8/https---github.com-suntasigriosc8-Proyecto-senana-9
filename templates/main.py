from inventario import Inventario, Producto

def menu():
    inventario = Inventario()
    while True:
        print("\n--- Menú de Inventario ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id = int(input("ID: "))
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            producto = Producto(id, nombre, cantidad, precio)
            inventario.agregar_producto(producto)
            print("Producto agregado.")
        elif opcion == "2":
            id = int(input("ID del producto a eliminar: "))
            inventario.eliminar_producto(id)
            print("Producto eliminado.")
        elif opcion == "3":
            id = int(input("ID del producto a actualizar: "))
            cantidad = int(input("Nueva cantidad: "))
            precio = float(input("Nuevo precio: "))
            inventario.actualizar_producto(id, cantidad, precio)
            print("Producto actualizado.")
        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            productos = inventario.buscar_por_nombre(nombre)
            for p in productos:
                print(p)
        elif opcion == "5":
            productos = inventario.mostrar_todos()
            for p in productos:
                print(p)
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()