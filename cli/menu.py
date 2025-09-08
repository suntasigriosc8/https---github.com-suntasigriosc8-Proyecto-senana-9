from inventario import Inventario, Producto

def menu():
    inventario = Inventario()
    try:
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
                ok = inventario.agregar_producto(producto)
                print("Producto agregado." if ok else "ID ya existe. No se agregó.")
            elif opcion == "2":
                id = int(input("ID del producto a eliminar: "))
                ok = inventario.eliminar_producto(id)
                print("Producto eliminado." if ok else "No existe el ID.")
            elif opcion == "3":
                id = int(input("ID del producto a actualizar: "))
                cantidad = input("Nueva cantidad (enter para mantener): ")
                precio = input("Nuevo precio (enter para mantener): ")
                cantidad_val = int(cantidad) if cantidad.strip() != "" else None
                precio_val = float(precio) if precio.strip() != "" else None
                ok = inventario.actualizar_producto(id, cantidad_val, precio_val)
                print("Producto actualizado." if ok else "No existe el ID.")
            elif opcion == "4":
                nombre = input("Nombre a buscar: ")
                productos = inventario.buscar_por_nombre(nombre)
                for p in productos:
                    print(p)
                if not productos:
                    print("No se encontraron productos.")
            elif opcion == "5":
                productos = inventario.mostrar_todos()
                for p in productos:
                    print(p)
                if not productos:
                    print("Inventario vacío.")
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
    finally:
        inventario.cerrar()

if __name__ == "__main__":
    menu()