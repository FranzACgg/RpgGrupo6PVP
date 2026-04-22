import os
import random
import msvcrt # Librería para detectar teclas sin Enter (solo Windows)

# Fundamentos Principales
# Tamaño del mapa
MAPA_REAL_ALTO = 50 
MAPA_REAL_ANCHO = 50

# Definimos el tamaño de lo que se VE en pantalla (la cámara)
CAMARA_ALTO = 10
CAMARA_ANCHO = 20

# Posicion del personaje 
pos_p = [1, 1] # Fila, Columna
inventario = []
#Tipos de Items
#Maatriz de Items 1: 1 Fila Pociones Buenas 2: 2 Fila Items Buenos : 3 Fila Equipamiento Bueno : 4 Fila Pociones Malas 2: 5 Fila Items Malos : 6 Fila Equipamiento Malo 
#Matriz 6 x 3 

#Que deberiamos agregar?, Estaria bueno la pocion de duda xd
items = [["Pocion de Fuerza Grande","Pocion de HP pequeña","Poción de HP Grande"],
         ["Gema de vida","Hacha de Mitril","Latigo con Puas"],
         ["Escudo de Obsidiana","Caso de Tungsteno","Pechera de escamas de Dragon"],
         ["Pocion Alucinogena","Pocion de Potencia / Impotencia","Pocion de I have no enemies"],
         ["Escudo del Heroe ;)","Lanza Maldita","Espada de Doble Filo Maldita"],
         ["Collar Paralizante","Guantes Benevolentes","Casco de Dullahan"]
         ]


TECLAS_MOVIMIENTO = ['w', 'a', 's', 'd']
TECLAS_ACCION = ['e', 'i', 'q'] # E para interactuar, I para inventario, Q salir




# 1. CREAR EL MAPA (Matriz)
def generar_mapa():
    # Creamos una matriz llena de espacios vacíos ' '
    mapa = [[" " for _ in range(MAPA_REAL_ANCHO)] for _ in range(MAPA_REAL_ALTO)]
    
    # Ponemos paredes '#' en los bordes
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if f == 0 or f == MAPA_REAL_ALTO-1 or c == 0 or c == MAPA_REAL_ANCHO-1:
                mapa[f][c] = "#"
    
    # Colocamos 3 ítems '*' en lugares aleatorios (que no sean paredes ni la pos inicial)
    for _ in range(3):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = "*"
        
    mapa[pos_p[0]][pos_p[1]] = "P" # Colocamos al jugador
    return mapa

mapa_actual = generar_mapa()

def dibujar_con_camara():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Calculamos el inicio de la "ventana" para que P esté en el centro
    inicio_f = max(0, min(pos_p[0] - CAMARA_ALTO // 2, MAPA_REAL_ALTO - CAMARA_ALTO))
    inicio_c = max(0, min(pos_p[1] - CAMARA_ANCHO // 2, MAPA_REAL_ANCHO - CAMARA_ANCHO))

    print(f"=== GLASSTION: EXPLORANDO ({pos_p[0]},{pos_p[1]}) ===")
    
    # Solo recorremos y dibujamos el pedacito que entra en la cámara
    for f in range(inicio_f, inicio_f + CAMARA_ALTO):
        fila_visible = mapa_actual[f][inicio_c : inicio_c + CAMARA_ANCHO]
        print(" ".join(fila_visible))
    
    


# 2. FUNCIÓN PARA MOSTRAR EL MAPA
def dibujar():
    os.system('cls' if os.name == 'nt' else 'clear') # ESTO ES CLAVE para que se vea estático
    print("=== GLASSTION: MODO RECOLECCIÓN ===")
    for fila in mapa_actual:
        print(" ".join(fila))
   

# 3. LÓGICA DE MOVIMIENTO
def mover(tecla):
    global pos_p
    df, dc = 0, 0
    if tecla == 'w': df = -1
    elif tecla == 's': df = 1
    elif tecla == 'a': dc = -1
    elif tecla == 'd': dc = 1
    else: return

    nueva_f = pos_p[0] + df
    nueva_c = pos_p[1] + dc
    

    # Verificamos colisión con pared
    if mapa_actual[nueva_f][nueva_c] != "#":
        # Si hay un ítem, lo recolectamos
        if mapa_actual[nueva_f][nueva_c] == "*":
            respuesta = ""
            respuesta = input("¿Deseas Recoger el Objeto? S/N: ")
            if respuesta == "s" or respuesta == "S":
                inventario.append(items[random.randint(0,5)][random.randint(0,2)])
                
        
        # Actualizamos matriz: borramos viejo, ponemos nuevo
        mapa_actual[pos_p[0]][pos_p[1]] = " "
        pos_p = [nueva_f, nueva_c]
        mapa_actual[pos_p[0]][pos_p[1]] = "P"

# ... (Mantené tus variables ANCHO, ALTO y pos_p igual) ...

def obtener_tecla():
    # msvcrt.getch() lee un byte de la tecla presionada
    # .decode() lo transforma en un string normal
    char = msvcrt.getch().decode('utf-8').lower()
    return char

def mostrar_inventario():
    print(inventario)


def procesar_entrada(tecla):
    
    # VALIDACIÓN: ¿Está la tecla en nuestro "diccionario" de permitidas?
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla)
    elif tecla == 'o':
        pantalla_menu_en_juego()
    
    # Si no es ninguna, el juego no hace nada y sigue el bucle
    return "continuar"

def pantalla_menu_en_juego():
    en_menu = True
    
    while en_menu:
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("=== MENÚ DE OPCIONES ===")
        print("I - Mostrar Inventario")
        print("E - Equipamiento")
        print("V - Volver al Juego")
        print("Q - Salir del Juego")
        print("========================")
        
        # Usamos obtener_tecla() para que sea instantáneo como el movimiento
        opcion = obtener_tecla() 

        if opcion == "i":
            mostrar_inventario()
            input("\nPresioná Enter para volver al menú...") # Pausa para leer
        elif opcion == "e":
            print("\nAun no está listo...")
            input("\nPresioná Enter para continuar...")
        elif opcion == "v":
            en_menu = False # Esto rompe el bucle del menú y vuelve al mapa
        elif opcion == "q":
            print("\nSaliendo del juego...")
            exit() # Cierra el programa por completo
        
# BUCLE PRINCIPAL
while True:
    dibujar_con_camara()   
    # getch() PAUSA el programa hasta que toques una tecla
    # Agregamos un try/except por si tocan teclas raras (Clase 10 del cronograma)
    
    print("====================================")
    print("Controles: WASD | Vida = 100/100 | TP = 50/50 || Opciones: O")
    tecla = obtener_tecla()
    procesar_entrada(tecla)
    
    