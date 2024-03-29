from datetime import datetime
import re
import graphviz

class PetManager:
    def __init__(self):
        self.mascotas = {}

    def ejecutar_comando(self, comando):
        instruccion = comando[0]
        if instruccion == "Crear_Gato":
            self.crear_gato(comando[1])
        elif instruccion == "Dar_de_Comer":
            if len(comando) >= 3:
                self.dar_de_comer(comando[1], int(comando[2]))
            else:
                print("El comando Dar_de_Comer no tiene suficientes parámetros.")
        elif instruccion == "Jugar":
            if len(comando) >= 3:  
                self.jugar_con_mascota(comando[1], int(comando[2]))
            else:
                print("El comando Jugar no tiene suficientes parámetros.")
        elif instruccion == "Resumen_Mascota":
            self.resumen_mascota(comando[1])
        elif instruccion == "Resumen_Global":
            self.resumen_global()
            
    def crear_gato(self, nombre):
        self.mascotas[nombre] = {"energia": 1, "vivo": True}
        self._escribir_en_archivo("mascotas.petmanager_result", f"Se creo el gato {nombre}")

    def dar_de_comer(self, nombre, peso):
        if nombre in self.mascotas:
            energia_aumentada = 12 + peso
            self.mascotas[nombre]["energia"] += energia_aumentada
            if self.mascotas[nombre]["energia"] <= 0:
                self.mascotas[nombre]["vivo"] = False
                self._escribir_en_archivo(f"mascotas.petmanager_result", {nombre}, "Muy tarde. Ya me mori despues de comer.")
            else:
                self._escribir_en_archivo("mascotas.petmanager_result", f"{nombre}, gracias ahora mi energia es {self.mascotas[nombre]['energia']}")
        else:
            print(f"[{datetime.now()}] No se encontró la mascota con nombre {nombre}")

    def jugar_con_mascota(self, nombre, tiempo):
        if nombre in self.mascotas:
            if isinstance(tiempo, int):
                energia_perdida_por_tiempo = int(0.1 * tiempo)
            self.mascotas[nombre]["energia"] -= energia_perdida_por_tiempo
            if self.mascotas[nombre]["energia"] <= 0:
                self.mascotas[nombre]["energia"] = 0
                self.mascotas[nombre]["vivo"] = False
                self._escribir_en_archivo("mascotas.petmanager_result", f"{nombre} Muy tarde. Ya me mori despues de jugar.")
            else:
                self._escribir_en_archivo("mascotas.petmanager_result", f"{nombre}, gracias por jugar conmigo ahora mi energia es {self.mascotas[nombre]['energia']}")
        else:
            print(f"[{datetime.now()}] No se encontró la mascota con nombre {nombre}")

    def resumen_mascota(self, nombre):
        if nombre in self.mascotas:
            estado = "Vivo" if self.mascotas[nombre]["vivo"] else "Muerto"
            self._escribir_en_archivo("mascotas.petmanager_result", f"{nombre}, Energia: {self.mascotas[nombre]['energia']}, Gato, {estado}")
        else:
            print(f" No se encontró la mascota con nombre {nombre}")

    def resumen_global(self):
        resumen = "------------------Resumen Global------------------\n"
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        for nombre, gato in self.mascotas.items():
            estado = "Vivo" if gato["vivo"] else "Muerto"
            resumen += f"[{fecha_actual}] {nombre}, Energia: {gato['energia']}, Gato, {estado}\n"
        self._escribir_en_archivo("mascotas.petmanager_result", resumen)
        self.generar_grafico()

    def generar_grafico(self):
        dot = graphviz.Digraph(comment='Mascotas')
        for nombre, gato in self.mascotas.items():
            dot.node(nombre, shape='ellipse', label=nombre)
            dot.node(f"{nombre}_energia", label=f"Energia: {gato['energia']}", shape='ellipse')
            dot.node(f"{nombre}_tipo", label="Tipo: Gato", shape='ellipse')
            dot.node(f"{nombre}_estado", label=f"Estado: {'Vivo' if gato['vivo'] else 'Muerto'}", shape='ellipse')
            dot.edge(nombre, f"{nombre}_energia")
            dot.edge(nombre, f"{nombre}_tipo")
            dot.edge(nombre, f"{nombre}_estado")
        dot.render('mascotas', format='png', cleanup=True)

    def _escribir_en_archivo(self, nombre_archivo, contenido):
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        with open(nombre_archivo, 'a') as archivo:
            archivo.write(f"[{fecha_actual}] {contenido}\n")

def leer_archivo(pet_manager):
    prueba = input("Ingresa el nombre del archivo .petmanager: ")
    try:
        with open(prueba, 'r') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                comando = re.split(r':|,', linea.strip())
                pet_manager.ejecutar_comando(comando)
    except FileNotFoundError:
        print("El archivo especificado no existe.")
