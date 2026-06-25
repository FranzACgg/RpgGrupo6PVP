import os
import msvcrt

from persistencia import existe_partida_guardada

ANCHO_UI = 80

limpiar = lambda: os.system("cls" if os.name == "nt" else "clear")


def mostrar_logo():
    print(r"""
 @@@@@@@  @       @@@@@@   @@@@@@   @@@@@@  @@@@@@@  \___/  @@@@@@  @   @@
 @        @      @      @ @        @           @       X   @      @ @@  @
 @  @@@@  @      @@@@@@@@  @@@@@@   @@@@@@     @      / \  @      @ @ @ @
 @     @  @      @      @       @        @     @     /   \ @      @ @  @@
  @@@@@@  @@@@@@ @      @ @@@@@@   @@@@@@      @     -----  @@@@@@  @   @
    """)


def mostrar_salon_heroes():
    heroes = {
        "Ragnar": {
            "Clase": "Guerrero",
            "Desc": "Gran defensa y mucha vida.",
            "Icono": "[Shield]",
        },
        "Morgan": {
            "Clase": "Pirata",
            "Desc": "Ataques impredecibles y fuerza.",
            "Icono": "[Sword]",
        },
        "Loki": {
            "Clase": "Bufón",
            "Desc": "Rápido, escurridizo y usa trucos.",
            "Icono": "[Magic]",
        },
    }

    limpiar()
    print("=" * ANCHO_UI)
    print(f"{'--- SALÓN DE HÉROES ---':^80}")
    print("=" * ANCHO_UI)

    for nombre, datos in heroes.items():
        print(
            f" {datos['Icono']} {nombre.upper():<10} | {datos['Clase']:<10} | {datos['Desc']}"
        )

    print("-" * ANCHO_UI)
    print(f"{'[Presioná cualquier tecla para volver al menú]':^80}")
    msvcrt.getch()


def mostrar_creditos():
    autores = [
        "Franz Acevedo",
        "Juan Colonia",
        "Tomas Perez",
        "Facundo Zambrana",
    ]
    limpiar()
    print(f"{'--- CREADORES DE GLASSTION ---':^80}")
    print("-" * ANCHO_UI)
    for nombre in autores:
        print(f"{nombre:^80}")
    print("-" * ANCHO_UI)
    print(f"\n{'[Presioná cualquier tecla para volver]':^80}")
    msvcrt.getch()


def confirmar_sobrescribir():
    limpiar()
    print(f"{'YA EXISTE UNA PARTIDA GUARDADA':^80}")
    print("-" * ANCHO_UI)
    print(f"{'Si empezas una nueva, se borra la guardada.':^80}")
    print(f"{'Continuar? [S/N]':^80}")
    tecla = msvcrt.getch().decode("utf-8").lower()
    return tecla == "s"


def menu_principal():
    cursor = 0
    while True:
        opciones = []
        if existe_partida_guardada():
            opciones.append("CONTINUAR")
        opciones.append("NUEVA PARTIDA")
        opciones.append("SALON DE HEROES")
        opciones.append("CREDITOS")
        opciones.append("SALIR")

        if cursor >= len(opciones):
            cursor = len(opciones) - 1

        limpiar()
        mostrar_logo()
        print(f"{'MENU PRINCIPAL':^80}")
        print("-" * ANCHO_UI)
        for i in range(len(opciones)):
            if i == cursor:
                print(f"  ==>  [ {opciones[i]} ]  <==  ".center(ANCHO_UI))
            else:
                print(f"       {opciones[i]}       ".center(ANCHO_UI))
        print("-" * ANCHO_UI)
        print(f"{'[W/S] Moverse  -  [Enter] Seleccionar':^80}")

        tecla = msvcrt.getch().decode("utf-8").lower()
        if tecla == "w" and cursor > 0:
            cursor -= 1
        elif tecla == "s" and cursor < len(opciones) - 1:
            cursor += 1
        elif tecla == "\r":
            seleccion = opciones[cursor]
            if seleccion == "CONTINUAR":
                return "continuar"
            elif seleccion == "NUEVA PARTIDA":
                if existe_partida_guardada() and not confirmar_sobrescribir():
                    continue
                return "nueva"
            elif seleccion == "SALON DE HEROES":
                mostrar_salon_heroes()
            elif seleccion == "CREDITOS":
                mostrar_creditos()
            elif seleccion == "SALIR":
                return "salir"


if __name__ == "__main__":
    menu_principal()
