import os

# Funcion para limpiar la consola y que el texto se vea prolijo
# Es una funcion lambda que limpia la pantalla segun tu sistema (Windows o Linux)
limpiar = lambda: os.system('cls' if os.name == 'nt' else 'clear')

# TUPLAS: Guardamos los mensajes fijos del comerciante (Unidad IV)
# Posicion 0: Saludo, Posicion 1: Pala, Posicion 2: Comercio, Posicion 3: Despedida
TEXTOS_MERCADER = (
    "Hola! No te habia visto por este cementerio. Buscas algo en especial?",
    "Una pala? Dicen que hay una enterrada cerca de la tumba real, pero es muy vieja.",
    "Si encontras tesoros, traelos aca. Yo te los cambio por buen oro.",
    "Suerte ahi afuera, la vas a necesitar."
)

def conversar_con_comerciante():
    # Tupla con las opciones del menu
    opciones = ("Saludar", "Preguntar por la pala", "Hablar de comercio", "Irse")
    charlando = True

    while charlando:
        limpiar()
        print("=== TIENDA DEL CEMENTERIO ===")
        
        # ARREGLO IMAGEN 1: Aqui ponemos la bienvenida usando el indice 0
        # Al poner  evitamos que se vea la tupla entera con parentesis
        print(f"Mercader: {TEXTOS_MERCADER}")
        print("-" * 35)
        
        # Recorremos la tupla de opciones para mostrarlas (Clase 1)
        for i in range(len(opciones)):
            print(f"{i + 1}. {opciones[i]}")

        # Bloque try/except para capturar errores si el usuario no pone un numero (Clase 8)
        try:
            entrada = input("\nQue quieres hacer? (Escribi el numero): ")
            seleccion = int(entrada)

            # ARREGLO IMAGEN 2: Usamos indices para responder una sola frase
            if seleccion == 1:
                # Mostramos solo el mensaje de la posicion 0
                print(f"\nRespuesta: {TEXTOS_MERCADER}")
            elif seleccion == 2:
                # Mostramos solo el mensaje de la posicion 1
                print(f"\nRespuesta: {TEXTOS_MERCADER[4]}")
            elif seleccion == 3:
                # Mostramos solo el mensaje de la posicion 2
                print(f"\nRespuesta: {TEXTOS_MERCADER[5]}")
            elif seleccion == 4:
                # Mostramos solo el mensaje de la posicion 3
                print(f"\nRespuesta: {TEXTOS_MERCADER[6]}")
                charlando = False # Cortamos el bucle para salir
            else:
                print("\nEse numero no esta en las opciones.")

            if charlando:
                input("\n[Presiona Enter para continuar]")

        # Si el usuario escribe una letra, el programa no se rompe y avisa del error
        except ValueError:
            print("\nError: Tenes que ingresar el numero de la opcion.")
            input("[Presiona Enter para reintentar]")

# Punto de inicio para ejecutar el sistema de dialogos
if __name__ == "__main__":
    conversar_con_comerciante()