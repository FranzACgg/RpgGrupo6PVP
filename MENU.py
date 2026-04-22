# --- PROYECTO GLASSTION ---
import os
import msvcrt 

# Definimos el ancho de banda visual para que el centrado sea prolijo en toda la interfaz
ANCHO_UI = 80

# Una funcion lambda cortita para limpiar la pantalla.
# Se usa para borrar lo anterior y que el menu parezca una animacion al moverse
limpiar = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_logo():
    print("""
 @@@@@@@  @       @@@@@@   @@@@@@   @@@@@@  @@@@@@@  \___/  @@@@@@  @   @@
 @        @      @      @ @        @           @       X   @      @ @@  @
 @  @@@@  @      @@@@@@@@  @@@@@@   @@@@@@     @      / \  @      @ @ @ @
 @     @  @      @      @       @        @     @     /   \ @      @ @  @@
  @@@@@@  @@@@@@ @      @ @@@@@@   @@@@@@      @     -----  @@@@@@  @   @
    """)

def mostrar_salon_heroes():
    # Usamos un diccionario anidado para mapear los stats y descripciones de los heroes
    # Esta estructura de clave:valor es para organizar la "fichas" de personajes
    heroes = {
        "Ragnar": {"Clase": "Guerrero", "Desc": "Gran defensa y mucha vida.", "Icono": "[Shield]"},
        "Morgan": {"Clase": "Pirata", "Desc": "Ataques impredecibles y fuerza.", "Icono": "[Sword]"},
        "Loki":   {"Clase": "Bufón", "Desc": "Rápido, escurridizo y usa trucos.", "Icono": "[Magic]"}
    }
    
    limpiar()
    print("=" * ANCHO_UI)
    print(f"{'--- SALÓN DE HÉROES ---':^80}")
    print("=" * ANCHO_UI)
    
    # Recorremos el diccionario usando el metodo .items()
    for nombre, datos in heroes.items():
        # CLASE 3: Formateo con f-strings para que los datos queden alineados
        print(f" {datos['Icono']} {nombre.upper():<10} | {datos['Clase']:<10} | {datos['Desc']}")
    
    print("-" * ANCHO_UI)
    print(f"{'[Presioná cualquier tecla para volver al menú]':^80}")
    msvcrt.getch() # Pausamos el flujo hasta detectar un evento de teclado

def mostrar_creditos():
    # Lista simple con los integrantes del Grupo
    autores = ["Franz Acevedo", "Juan Colonia", "Tomas Perez", "Facundo Zambrana"]
    limpiar()
    print(f"{'--- CREADORES DE GLASSTION ---':^80}")
    print("-" * ANCHO_UI)
    for nombre in autores:
        # Centramos cada nombre dinamicamente
        print(f"{nombre:^80}")
    print("-" * ANCHO_UI)
    print(f"\n{'[Presioná cualquier tecla para volver]':^80}")
    msvcrt.getch()

def menu_principal():
    # Estructura de datos (lista) para gestionar los estados del menu
    opciones = ["EMPEZAR", "SALÓN DE HÉROES", "CRÉDITOS", "SALIR"]
    cursor = 0 # Puntero entero que rastrea el indice de la opcion seleccionada
    
    while True:
        limpiar()
        mostrar_logo()
        
        print(f"{'MENU PRINCIPAL':^80}")
        print("-" * ANCHO_UI)
        
        # Iteramos con range y len para renderizar la opción con feedback visual
        for i in range(len(opciones)):
            if i == cursor:
                # Si el índice coincide con el puntero, le metemos las flechitas
                print(f"  ==>  [ {opciones[i]} ]  <==  ".center(ANCHO_UI))
            else:
                print(f"       {opciones[i]}       ".center(ANCHO_UI))
        
        print("-" * ANCHO_UI)
        print(f"{'[W/S] Moverse  -  [Enter] Seleccionar':^80}")

        # Capturamos la tecla que toca el usuario
        # .decode('utf-8') sirve para pasar el dato de la tecla a texto comun
        tecla = msvcrt.getch().decode('utf-8').lower()
        
        # Logica para mover el cursor (subir o bajar en la lista)
        if tecla == 'w' and cursor > 0:
            cursor -= 1
        elif tecla == 's' and cursor < len(opciones) - 1:
            cursor += 1
        elif tecla == '\r': # El caracter '\r' representa la tecla Enter
            if cursor == 0:
                print(f"\n{'CARGANDO AVENTURA...':^80}")
                break # Sale del menu para empezar el juego
            elif cursor == 1:
                mostrar_salon_heroes()
            elif cursor == 2:
                mostrar_creditos()
            elif cursor == 3:
                print(f"\n{'CERRANDO EL LIBRO DE GLASSTION...':^80}")
                break

if __name__ == "__main__":
    menu_principal()