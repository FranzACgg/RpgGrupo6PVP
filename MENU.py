# --- PROYECTO GLASSTION ---
# Menu principal provisional (Agregar mas cosas)

# Definimos una función lambda para manejar las vidas
# Esta recibe las 'iniciales' y las 'perdidas', y devuelve el resultado de la resta
# Es ideal para calculos rápidos como este del "collar de resurrección"
calcular_vidas = lambda iniciales, perdidas: iniciales - perdidas

def mostrar_logo():
    print("""
  _____  _               _____  _____ _______ _____ ____  _   _ 
 / ____|| |        /\   / ____|/ ____|__   __|_   _/ __ \| \ | |
| |  __ | |       /  \ | (___ | (___    | |    | || |  | |  \| |
| | |_ || |      / /\ \ \___ \ \___ \   | |    | || |  | | . ` |
| |__| || |____ / ____ \____) |____) |  | |   _| || |__| | |\  |
 \_____||______/_/    \_\_____/|_____/   |_|  |_____\____/|_| \_|
    """) # Logo ASCII del titulo de juego

def menu_principal():
    # Guardamos las opciones del menu en una lista
    opciones = ["EMPEZAR", "SALIR"]
    
    # Multiplicamos el string "-" por 66 para crear una línea 
    # decorativa sin tener que escribir el guion 66 veces a mano
    linea_decorativa = "-" * 66
    
    # Este bucle 'while' mantiene el menú abierto hasta que el usuario decida salir
    ejecutando = True
    while ejecutando:
        mostrar_logo()
        
        print(linea_decorativa)
        
        # Usamos un ciclo 'for' para recorrer la lista de opciones.
        # Usamos 'range(len(opciones))' para obtener los indices (0, 1, etc.)
        # y poder mostrar [5], [6], etc., al usuario
        for i in range(len(opciones)):
            print(f"[{i + 1}] {opciones[i]}")
        
        print(linea_decorativa)
        
        # Pedimos al usuario que elija una opcion
        seleccion = input("Seleccione su destino: ")
        
        # Logica de decision del jugador con 'if' y 'elif'
        if seleccion == "1":
            print("\n" + "*" * 20)
            # Aca usamos la función lambda que definimos arriba.
            # Le pasamos 3 (vidas iniciales) y 0 (todavía no murio)
            vidas_actuales = calcular_vidas(3, 0)
            print(f"DESPERTANDO EN EL CEMENTERIO... Vidas restantes: {vidas_actuales}")
            print("*" * 20)
            # Cortamos el bucle para que parezca que entramos al juego.
            ejecutando = False 
            
        elif seleccion == "2":
            # Si elige 2, simplemente nos despedimos y cerramos el bucle.
            print("Cerrando el libro de Glasstion... Nos vemos.")
            ejecutando = False
            
        else:
            # Si pone cualquier otra cosa, le avisamos que se equivoco
            print("\n[!] Esa opción no es válida en este coliseo. Intentá de nuevo.")

# Punto de entrada del programa para que todo arranque en orden.
if __name__ == "__main__":
    menu_principal()