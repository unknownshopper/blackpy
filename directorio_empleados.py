import json
import os
from datetime import datetime

class DirectorioEmpleados:
    def __init__(self, archivo_datos="empleados.json"):
        self.archivo_datos = archivo_datos
        self.empleados = []
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos desde el archivo JSON si existe."""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                    self.empleados = json.load(archivo)
            except json.JSONDecodeError:
                print("Error al cargar el archivo. Iniciando con lista vacía.")
                self.empleados = []
        else:
            self.empleados = []
    
    def guardar_datos(self):
        """Guarda los datos en el archivo JSON."""
        with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
            json.dump(self.empleados, archivo, indent=4, ensure_ascii=False)
    
    def agregar_empleado(self, nombre, apellido, cargo, departamento, fecha_ingreso=None):
        """Agrega un nuevo empleado al directorio."""
        if fecha_ingreso is None:
            fecha_ingreso = datetime.now().strftime("%Y-%m-%d")
        
        nuevo_empleado = {
            "id": len(self.empleados) + 1,
            "nombre": nombre,
            "apellido": apellido,
            "cargo": cargo,
            "departamento": departamento,
            "fecha_ingreso": fecha_ingreso,
            "fecha_despido": "",
            "motivo_despido": ""
        }
        
        self.empleados.append(nuevo_empleado)
        self.guardar_datos()
        return nuevo_empleado
    
    def listar_todos(self):
        """Retorna la lista completa de empleados (solo para administradores)."""
        return self.empleados
    
    def buscar_por_nombre(self, texto):
        """Busca empleados por nombre o apellido."""
        texto = texto.lower()
        resultados = []
        
        for empleado in self.empleados:
            if (texto in empleado["nombre"].lower() or 
                texto in empleado["apellido"].lower()):
                resultados.append(empleado)
        
        return resultados
    
    def buscar_por_departamento(self, departamento):
        """Busca empleados por departamento."""
        departamento = departamento.lower()
        return [e for e in self.empleados if departamento in e["departamento"].lower()]
    
    def buscar_por_cargo(self, cargo):
        """Busca empleados por cargo."""
        cargo = cargo.lower()
        return [e for e in self.empleados if cargo in e["cargo"].lower()]
        
    def buscar_por_id(self, id):
        """Busca un empleado por su ID."""
        for empleado in self.empleados:
            if empleado["id"] == id:
                return empleado
        return None
        
    def editar_empleado(self, id, nombre, apellido, cargo, departamento):
        """Edita un empleado existente."""
        empleado = self.buscar_por_id(id)
        if empleado:
            empleado["nombre"] = nombre
            empleado["apellido"] = apellido
            empleado["cargo"] = cargo
            empleado["departamento"] = departamento
            self.guardar_datos()
            return True
        return False
        
    def eliminar_empleado(self, id):
        """Elimina un empleado por su ID."""
        empleado = self.buscar_por_id(id)
        if empleado:
            self.empleados.remove(empleado)
            self.guardar_datos()
            return True
        return False
    
    def registrar_despido(self, id, fecha_despido, motivo_despido):
        """Registra la fecha y motivo de despido de un empleado."""
        empleado = self.buscar_por_id(id)
        if empleado:
            empleado["fecha_despido"] = fecha_despido
            empleado["motivo_despido"] = motivo_despido
            self.guardar_datos()
            return True
        return False


class InterfazUsuario:
    def __init__(self):
        self.directorio = DirectorioEmpleados()
        self.es_admin = False
    
    def iniciar_sesion(self):
        """Maneja el inicio de sesión para determinar el tipo de usuario."""
        print("\n===== SISTEMA DE DIRECTORIO DE EMPLEADOS =====")
        print("1. Iniciar sesión como Administrador")
        print("2. Iniciar sesión como Usuario")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            password = input("Ingrese la contraseña de administrador: ")
            # En un sistema real, verificaríamos la contraseña de forma segura
            # Para este ejemplo, usamos "admin123" como contraseña
            if password == "admin123":
                self.es_admin = True
                print("Inicio de sesión como administrador exitoso.")
                self.menu_principal()
            else:
                print("Contraseña incorrecta.")
                self.iniciar_sesion()
        elif opcion == "2":
            self.es_admin = False
            print("Inicio de sesión como usuario regular exitoso.")
            self.menu_principal()
        elif opcion == "3":
            print("¡Hasta pronto!")
            return
        else:
            print("Opción inválida. Intente nuevamente.")
            self.iniciar_sesion()
    
    def menu_principal(self):
        """Muestra el menú principal según el tipo de usuario."""
        while True:
            print("\n===== MENÚ PRINCIPAL =====")
            
            if self.es_admin:
                print("1. Agregar nuevo empleado")
                print("2. Ver lista completa de empleados")
                print("3. Buscar empleados")
                print("4. Cerrar sesión")
                print("5. Salir")
                
                opcion = input("\nSeleccione una opción: ")
                
                if opcion == "1":
                    self.agregar_empleado()
                elif opcion == "2":
                    self.listar_empleados()
                elif opcion == "3":
                    self.menu_busqueda()
                elif opcion == "4":
                    self.es_admin = False
                    print("Sesión cerrada.")
                    self.iniciar_sesion()
                    return
                elif opcion == "5":
                    print("¡Hasta pronto!")
                    return
                else:
                    print("Opción inválida. Intente nuevamente.")
            else:
                # Menú para usuario regular
                print("1. Buscar empleados")
                print("2. Cerrar sesión")
                print("3. Salir")
                
                opcion = input("\nSeleccione una opción: ")
                
                if opcion == "1":
                    self.menu_busqueda()
                elif opcion == "2":
                    print("Sesión cerrada.")
                    self.iniciar_sesion()
                    return
                elif opcion == "3":
                    print("¡Hasta pronto!")
                    return
                else:
                    print("Opción inválida. Intente nuevamente.")
    
    def agregar_empleado(self):
        """Interfaz para agregar un nuevo empleado."""
        print("\n===== AGREGAR NUEVO EMPLEADO =====")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        cargo = input("Cargo: ")
        departamento = input("Departamento: ")
        
        empleado = self.directorio.agregar_empleado(nombre, apellido, cargo, departamento)
        print(f"\nEmpleado agregado exitosamente con ID: {empleado['id']}")
    
    def listar_empleados(self):
        """Muestra la lista completa de empleados (solo para administradores)."""
        if not self.es_admin:
            print("No tiene permisos para ver la lista completa.")
            return
        
        empleados = self.directorio.listar_todos()
        
        if not empleados:
            print("\nNo hay empleados registrados.")
            return
        
        print("\n===== LISTA COMPLETA DE EMPLEADOS =====")
        self.mostrar_empleados(empleados)
    
    def menu_busqueda(self):
        """Muestra el menú de búsqueda de empleados."""
        print("\n===== BUSCAR EMPLEADOS =====")
        print("1. Buscar por nombre o apellido")
        print("2. Buscar por departamento")
        print("3. Buscar por cargo")
        print("4. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            texto = input("Ingrese nombre o apellido a buscar: ")
            resultados = self.directorio.buscar_por_nombre(texto)
            self.mostrar_resultados(resultados)
        elif opcion == "2":
            departamento = input("Ingrese departamento a buscar: ")
            resultados = self.directorio.buscar_por_departamento(departamento)
            self.mostrar_resultados(resultados)
        elif opcion == "3":
            cargo = input("Ingrese cargo a buscar: ")
            resultados = self.directorio.buscar_por_cargo(cargo)
            self.mostrar_resultados(resultados)
        elif opcion == "4":
            return
        else:
            print("Opción inválida. Intente nuevamente.")
            self.menu_busqueda()
    
    def mostrar_resultados(self, resultados):
        """Muestra los resultados de una búsqueda."""
        if not resultados:
            print("\nNo se encontraron resultados.")
            return
        
        print(f"\nSe encontraron {len(resultados)} resultados:")
        self.mostrar_empleados(resultados)
    
    def mostrar_empleados(self, empleados):
        """Muestra una lista de empleados en formato tabular."""
        # Determinar el ancho máximo para cada columna
        max_id = max(len(str(e["id"])) for e in empleados)
        max_nombre = max(len(e["nombre"]) for e in empleados)
        max_apellido = max(len(e["apellido"]) for e in empleados)
        max_cargo = max(len(e["cargo"]) for e in empleados)
        max_departamento = max(len(e["departamento"]) for e in empleados)
        
        # Asegurar mínimos para los encabezados
        max_id = max(max_id, 2)  # "ID"
        max_nombre = max(max_nombre, 6)  # "Nombre"
        max_apellido = max(max_apellido, 8)  # "Apellido"
        max_cargo = max(max_cargo, 5)  # "Cargo"
        max_departamento = max(max_departamento, 12)  # "Departamento"
        
        # Imprimir encabezado
        print(f"\n{'ID'.ljust(max_id)} | {'Nombre'.ljust(max_nombre)} | {'Apellido'.ljust(max_apellido)} | "
              f"{'Cargo'.ljust(max_cargo)} | {'Departamento'.ljust(max_departamento)} | Fecha Ingreso")
        print("-" * (max_id + max_nombre + max_apellido + max_cargo + max_departamento + 30))
        
        # Imprimir cada empleado
        for e in empleados:
            print(f"{str(e['id']).ljust(max_id)} | {e['nombre'].ljust(max_nombre)} | "
                  f"{e['apellido'].ljust(max_apellido)} | {e['cargo'].ljust(max_cargo)} | "
                  f"{e['departamento'].ljust(max_departamento)} | {e['fecha_ingreso']}")


if __name__ == "__main__":
    interfaz = InterfazUsuario()
    interfaz.iniciar_sesion()