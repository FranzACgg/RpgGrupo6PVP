# --- PROYECTO GLASSTION ---
import os
import msvcrt 

# Definimos el ancho de la interfaz para que el centrado sea consistente
ANCHO_UI = 80 

# Una funcion lambda cortita para limpiar la pantalla
# Se usa para borrar lo anterior y que el menu parezca una animacion al moverse
limpiar = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_linea_con_borde(texto):
    # CLASE 3: Función auxiliar para meter texto entre las paredes del recuadro "║"
    # Usamos f-strings con el modificador "^" para centrar el contenido [2, 3]
    print(f"║{texto.center(ANCHO_UI)}║")

def mostrar_logo():
    logo = """
 @@@@@@@  @       @@@@@@   @@@@@@   @@@@@@  @@@@@@@  \___/  @@@@@@  @   @@
 @        @      @      @ @        @           @       X   @      @ @@  @
 @  @@@@  @      @@@@@@@@  @@@@@@   @@@@@@     @      / \  @      @ @ @ @
 @     @  @      @      @       @        @     @     /   \ @      @ @  @@
  @@@@@@  @@@@@@ @      @ @@@@@@   @@@@@@      @     -----  @@@@@@  @   @
    """
    # Imprimimos el logo línea por línea dentro del borde para que no se rompa el cuadro
    for linea in logo.strip("\n").split("\n"):
        imprimir_linea_con_borde(linea)

def mostrar_salon_heroes():
    # Usamos un diccionario anidado para mapear los stats y descripciones de los heroes
    # Esta estructura de clave:valor es para organizar la "fichas" de personajes
    heroes = {
        "Ragnar": {"Clase": "Guerrero", "Desc": "Gran defensa y mucha vida."},
        "Morgan": {"Clase": "Pirata", "Desc": "Ataques impredecibles."},
        "Loki":   {"Clase": "Bufón", "Desc": "Rápido y usa trucos."}
    }
    limpiar()
    print("╔" + "═" * ANCHO_UI + "╗")
    imprimir_linea_con_borde("--- SALÓN DE HÉROES ---")
    print("╠" + "═" * ANCHO_UI + "╣")
    
    # Recorremos el diccionario usando el metodo .items()
    for nombre, datos in heroes.items():
        imprimir_linea_con_borde(f"{nombre.upper()} ({datos['Clase']}): {datos['Desc']}")
    
    print("╚" + "═" * ANCHO_UI + "╝")
    print(f"{'[Presioná cualquier tecla para volver]':^80}")
    msvcrt.getch() # Pausamos el flujo hasta detectar un evento de teclado

def mostrar_creditos():
    # Lista simple con los integrantes del Grupo
    autores = ["Franz Acevedo", "Juan Colonia", "Tomas Perez", "Facundo Zambrana"]
    limpiar()
    print("╔" + "═" * ANCHO_UI + "╗")
    imprimir_linea_con_borde("--- CREADORES DE GLASSTION ---")
    print("╠" + "═" * ANCHO_UI + "╣")
    for autor in autores:
        imprimir_linea_con_borde(autor)
    print("╚" + "═" * ANCHO_UI + "╝")
    msvcrt.getch()

def menu_principal():
    # Estructura de datos (lista) para gestionar los estados del menu
    opciones = ["EMPEZAR", "SALÓN DE HÉROES", "CRÉDITOS", "SALIR"]
    cursor = 0 
    
    while True:
        limpiar()
        
        print("╔" + "═" * ANCHO_UI + "╗")
        
        # Metemos el logo adentro del recuadro
        mostrar_logo()
        
        print("╠" + "═" * ANCHO_UI + "╣")
        imprimir_linea_con_borde("MENU PRINCIPAL")
        print("╠" + "═" * ANCHO_UI + "╣")
        
        # Iteramos con range y len para renderizar la opción con feedback visual
        for i in range(len(opciones)):
            if i == cursor:
                # Feedback visual para la opción seleccionada
                imprimir_linea_con_borde(f"==> [ {opciones[i]} ] <==")
            else:
                imprimir_linea_con_borde(opciones[i])
        
        # Parte inferior del recuadro
        print("╚" + "═" * ANCHO_UI + "╝")
        print(f"{'[W/S] Moverse  -  [Enter] Elegir':^80}")

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
                print(f"\n{'DESPERTANDO EN EL CEMENTERIO...':^80}")
                break # Sale del menu para empezar el juego
            elif cursor == 1:
                mostrar_salon_heroes()
            elif cursor == 2:
                mostrar_creditos()
            elif cursor == 3:
                print(f"\n{'¡CERRANDO EL LIBRO DE GLASSTION!':^80}")
                break

if __name__ == "__main__":
    menu_principal()