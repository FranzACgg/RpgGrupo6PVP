import os

# Función para limpiar la pantalla y que no se amontone el texto
limpiar = lambda: os.system('cls' if os.name == 'nt' else 'clear')

# Usamos una tupla para los dialogos porque son mensajes fijos que no necesitamos modificar
TEXTOS_MERCADER = (
    "¡Hola! No te habia visto por este cementerio. ¿Buscas algo en especial?",
    "¿Una pala? Dicen que hay una enterrada cerca de la tumba real, pero es muy vieja.",
    "Si encontras tesoros, traelos aca. Yo te los cambio por buen oro.",
    "Suerte ahi afuera, la vas a necesitar."
)

def conversar_con_comerciante():
    # Opciones que el jugador puede elegir
    opciones = ("Saludar", "Preguntar por la pala", "Hablar de comercio", "Irse")
    charlando = True

    while charlando:
        limpiar()
        print("=== TIENDA DEL CEMENTERIO ===")
        print("Te acercas al mostrador del mercader.")
        print("-" * 30)

        # Recorremos la lista de opciones para mostrarlas numeradas
        for i in range(len(opciones)):
            print(f"{i + 1}. {opciones[i]}")

        # Este bloque 'try' intenta ejecutar el codigo y, si hay un error, lo atrapa
        try:
            # Pedimos el numero de opción al usuario
            entrada = input("\n¿Que queres hacer? (Escribi el numero): ")
            seleccion = int(entrada)

            # Logica para decidir que responder según el número elegido
            if seleccion == 1:
                print(f"\nMercader: '{TEXTOS_MERCADER[0]}'")
            elif seleccion == 2:
                print(f"\nMercader: '{TEXTOS_MERCADER[1]}'")
            elif seleccion == 3:
                print(f"\nMercader: '{TEXTOS_MERCADER[2]}'")
            elif seleccion == 4:
                print(f"\nMercader: '{TEXTOS_MERCADER[3]}'")
                charlando = False # Corta el bucle para salir de la charla
            else:
                # Si el numero no está entre 1 y 4, avisamos al usuario
                print("\nEse número no está en las opciones.")

            if charlando:
                input("\n[Presioná Enter para seguir hablando]")

        # Si el usuario escribio una letra en vez de un numero, se ejecuta este aviso
        except ValueError:
            print("\nError: Tenes que ingresar el número de la opción (ejemplo: 1).")
            input("[Presiona Enter para intentar de nuevo]")