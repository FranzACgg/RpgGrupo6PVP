import os
import msvcrt
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

INVENTARIO_MAXIMO = 30
ITEM_KEYS_VALUES = {
    "id_item": 0,
    "nombre": "",
    "tipo": "",
    "cantidad": 0,
    "equipado": False,
}

# cuantos items mostrar por pagina
ITEMS_POR_PAGINA = 8

# tipos de items tentativos: consumible, equipable, intercambiable, clave, usable

console = Console()  # Consola rich


# Logica del Inventario


def crear_inventario():
    """
    Objetivo: crear inventario.
    Salida: lista vacia
    """
    return []


def agregar_item(item, inventario):
    """
    Entrada: Diccionario , Lista
    Params:
        item: Diccionario con el item a agregar al inventario
        inventario: Lista con todos los items en el inventario
    Objetivo: Agregar item al inventario
    Salida: none. Modifica el inventario original que toma la funcion
    """
    if item.keys() != ITEM_KEYS_VALUES.keys():
        return print("Error, el objeto ingresado no tiene las keys de un item")
    i = busqueda_item_por_id(item["id_item"], inventario)
    if i != -1:
        inventario[i]["cantidad"] += 1
    else:
        if len(inventario) >= INVENTARIO_MAXIMO:
            return print("Inventario lleno")
        inventario.append(item.copy())


def busqueda_item_por_id(id_item, inventario):
    """
    Entrada: Entero, Lista
    Params:
        id_item: Id del item a buscar
        inventario: Lista con todos los items en el inventario
    Objetivo: Buscar items secuencialmente segun ID
    Salida: Numero entero (indice del slot donde esta el item buscado o -1 si el item no esta presente)
    """
    i = 0
    while i < len(inventario) and inventario[i]["id_item"] != id_item:
        i += 1
    if i < len(inventario):
        return i
    else:
        return -1


def usar_item(id_item, inventario):
    """
    Entrada: Entero, Lista
    Params:
        id_item: Id del item a usar
        inventario: Lista con todos los items en el inventario
    Objetivo: Manejar el uso de items
    Salida: Diccionario del item que se uso o none si hubo un error. Modifica el inventario original que toma la funcion
    """
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return None
    item = inventario[i]
    if item["tipo"] != "consumible":
        return None
    if item["cantidad"] <= 0:
        return None
    elif item["cantidad"] == 1:
        inventario.pop(i)
    else:
        item["cantidad"] -= 1
    return item


def manejar_equipado_item(id_item, inventario):
    """
    Entrada: Entero, Lista
    Params:
        id_item: Id del item a equipar/desequipar
        inventario: Lista con todos los items en el inventario
    Objetivo: equipar/desquipar items
    Salida: Diccionario con el item que se equipo / desquipo o none si hubo un error. Modifica el inventario original que toma la funcion
    """
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return None
    item = inventario[i]
    if item["tipo"] != "equipable":
        return None
    if item["cantidad"] <= 0:
        return None
    item["equipado"] = not item["equipado"]
    return item


def exportar_items_equipados(inventario):
    """
    Entrada: Lista
    Params:
        inventario: Lista con todos los items en el inventario
    Objetivo: exportar una lista con los items equipados
    Salida: lista de diccionarios con los items equipados
    """
    return [item for item in inventario if item["equipado"]]


def descartar_item(id_item, inventario):
    """
    Entrada: entero, lista
    Params:
        id_item: Id del item a descartar
        inventario: Lista con todos los items en el inventario
    Objetivo: descartar un item del inventario
    Salida: True/False s/exito de la operacion. Modifica el inventario original que toma la funcion
    """
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return False
    if inventario[i]["tipo"] == "clave":
        return False
    if inventario[i]["equipado"]:
        return False
    if inventario[i]["cantidad"] <= 0:
        return False
    if inventario[i]["cantidad"] > 1:
        inventario[i]["cantidad"] -= 1
        return True
    else:
        inventario.pop(i)
        return True


# UI del Inventario


def limpiar_consola():
    """
    Objetivo: limpiar consola según el sistema operativo
    nt = Windows, cls es el comando para limpiar la consola en Windows
    clear es el comando para limpiar la consola en Unix/Linux/Mac
    Salida: none
    """
    os.system("cls" if os.name == "nt" else "clear")


def obtener_tecla():
    """
    Objetivo: obtener una tecla sin necesidad de presionar enter (solo Windows) usando msvcrt
    msvcrt.getch() pausa el programa haste que el usuario presione usa tecla, luego devuelve un byte, este se decodifica a string en formato utf-8 y se convierte a minuscula para facilitar la comparación
    Salida: string (la tecla que se presionó)
    """
    return msvcrt.getch().decode("utf-8").lower()


def construir_cadenas_inventario(inventario, cursor, desvio_cursor):
    """
    Entrada: Lista, Entero, Entero
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
        desvio_cursor: Desde que posicion de la lista empezar a dibujar la pantalla
    Objetivo: Construir el texto del inventario para renderizar con Rich
    Salida: string con el contenido formateado
    """
    cadenas = []

    if len(inventario) == 0:
        cadenas.append(
            "[dim]~ Vacío ~[/]"
        )  # [dim]...[/] es markup de rich para texto grisado.
    else:
        if desvio_cursor + ITEMS_POR_PAGINA < len(inventario):
            rango = desvio_cursor + ITEMS_POR_PAGINA
        else:
            rango = len(inventario)

        for i in range(desvio_cursor, rango):
            selector = "[bold white]>[/] "
            if i != cursor:
                selector = "  "

            nombre = inventario[i]["nombre"]
<<<<<<< HEAD
            cantidad = f'x{inventario[i]["cantidad"]}'
            equipado = ' [bold cyan]\\[E][/]' if inventario[i]["equipado"] else '' # 
=======
            cantidad = f"x{inventario[i]['cantidad']}"
            equipado = (
                r" [bold cyan]\[E][/]" if inventario[i]["equipado"] else ""
            )  #
>>>>>>> origin/integracion_40

            if i == cursor:
                cadenas.append(
                    f"[bold white]{selector}{nombre:<26} {cantidad:>4}{equipado}[/]"
                )  # <26 padding izq  ; >4 padding derecha
            else:
                cadenas.append(
                    f"[dim]{selector}{nombre:<26} {cantidad:>4}{equipado}[/]"
                )

        if desvio_cursor > 0:
            cadenas.append("[dim]  ▲ más arriba[/]")
        if rango < len(inventario):
            cadenas.append("[dim]  ▼ más abajo[/]")

    return "\n".join(cadenas)


def construir_detalle(inventario, cursor):
    """
    Entrada: Lista, Entero
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
    Objetivo: Construir el texto del panel de detalle
    Salida: string con el contenido formateado
    """
    if len(inventario) == 0:
        return "[dim]Seleccioná un item para ver detalles[/]"

    item = inventario[cursor]
    detalle = f"[bold]{item['nombre']}[/]\n"
    detalle += f"[dim]Tipo:[/] {item['tipo']} [dim]|[/] [dim]Cantidad:[/] {item['cantidad']}"
    if item["tipo"] == "equipable":
        estado = (
            "[bold cyan]Equipado[/]"
            if item["equipado"]
            else "[dim]No equipado[/]"
        )
        detalle += f"\n[dim]Estado:[/] {estado}"
    return detalle


def construir_controles(inventario, cursor):
    """
    Entrada: Lista, Entero
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
    Objetivo: Construir el texto de controles disponibles
    Salida: string con el contenido formateado
    """
    if len(inventario) == 0:
        return "[dim]Q Cerrar[/]"

    item = inventario[cursor]
    controles = []
    if item["tipo"] == "consumible":
        controles.append("[bold green]U[/] Usar")
    if item["tipo"] == "equipable":
        if item["equipado"]:
            controles.append("[bold cyan]E[/] Desequipar")
        else:
            controles.append("[bold cyan]E[/] Equipar")
    if item["tipo"] != "clave" and not item["equipado"]:
        controles.append("[bold red]T[/] Tirar")

    linea1 = " [dim]|[/] ".join(controles) if controles else ""
    linea2 = "[dim]W/S[/] Navegar [dim]|[/] [dim]Q[/] Cerrar"

    if linea1:
        return f"{linea1}\n{linea2}"
    return linea2


def renderizar_inventario(inventario, cursor, desvio_cursor, mensaje=""):
    """
    Entrada: Lista, Entero, Entero, String
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
        desvio_cursor: Desde que posicion de la lista empezar a dibujar la pantalla
        mensaje: Mensaje temporal a mostrar (ej: "Usaste Pocion de HP")
    Objetivo: Renderizar el inventario completo centrado con Rich
    Salida: none
    """
    limpiar_consola()

    # Armar contenidos del inventario con markup de rich
    contenido_items = construir_cadenas_inventario(
        inventario, cursor, desvio_cursor
    )
    detalle = construir_detalle(inventario, cursor)
    controles = construir_controles(inventario, cursor)

    # Unir todo con separadores grises entre secciones
    separador = "[dim]─────────────────────────────────────────[/]"
    contenido_total = (
        f"{contenido_items}\n{separador}\n{detalle}\n{separador}\n{controles}"
    )

    if mensaje:
        contenido_total += f"\n\n[bold yellow]>> {mensaje}[/]"

    panel = Panel(
        contenido_total,
        title=f"[bold yellow]INVENTARIO ({len(inventario)}/{INVENTARIO_MAXIMO})[/]",
        border_style="bright_blue",
        expand=False,
        padding=(1, 2),
    )

    console.print(
        Align(
            panel,
            align="center",
            vertical="middle",
            height=console.size.height,
        )
    )


def manejar_inventario(inventario):
    """
    Entrada: Lista
    Params:
        inventario: Lista con todos los items en el inventario
    Objetivo: Maneja y coordina todas las operaciones del inventario
    Salida: none
    """
    tecla = ""
    cursor = 0
    desvio_cursor = 0
    mensaje = ""

    while tecla != "q":
        largo_original = len(inventario)
        renderizar_inventario(inventario, cursor, desvio_cursor, mensaje)
        mensaje = ""
        tecla = obtener_tecla()

        if len(inventario) > 0:
            id_item = inventario[cursor]["id_item"]

            if tecla == "w":
                if cursor != 0:
                    cursor -= 1
            elif tecla == "s":
                if cursor != len(inventario) - 1:
                    cursor += 1
            elif tecla == "u":
                item = usar_item(id_item, inventario)
                if item:
                    mensaje = f"Usaste {item['nombre']}"
                if len(inventario) < largo_original and cursor != 0:
                    cursor -= 1
            elif tecla == "e":
                item = manejar_equipado_item(id_item, inventario)
                if item:
                    estado = (
                        "Equipaste" if item["equipado"] else "Desequipaste"
                    )
                    mensaje = f"{estado} {item['nombre']}"
            elif tecla == "t":
                nombre_item = inventario[cursor]["nombre"]
                renderizar_inventario(
                    inventario,
                    cursor,
                    desvio_cursor,
                    f"Descartar {nombre_item}? [S/N]",
                )
                confirmacion = ""
                while confirmacion not in ["s", "n"]:
                    confirmacion = obtener_tecla()
                if confirmacion == "s":
                    descartar_item(id_item, inventario)
                    mensaje = f"Descartaste {nombre_item}"
                if len(inventario) < largo_original and cursor != 0:
                    cursor -= 1

        if cursor < desvio_cursor:
            desvio_cursor = cursor
        elif cursor >= desvio_cursor + ITEMS_POR_PAGINA:
            desvio_cursor += 1


# ── Pruebas ────────────────────────────────────────────────────

if __name__ == "__main__":
    inv = crear_inventario()

    items_prueba = [
        {
            "id_item": 1,
            "nombre": "Pocion de HP pequeña",
            "tipo": "consumible",
            "cantidad": 5,
            "equipado": False,
        },
        {
            "id_item": 2,
            "nombre": "Escudo de Obsidiana",
            "tipo": "equipable",
            "cantidad": 1,
            "equipado": False,
        },
        {
            "id_item": 3,
            "nombre": "Gema de vida",
            "tipo": "clave",
            "cantidad": 2,
            "equipado": False,
        },
        {
            "id_item": 4,
            "nombre": "Hacha de Mitril",
            "tipo": "equipable",
            "cantidad": 1,
            "equipado": True,
        },
        {
            "id_item": 5,
            "nombre": "Pocion de Fuerza Grande",
            "tipo": "consumible",
            "cantidad": 3,
            "equipado": False,
        },
        {
            "id_item": 6,
            "nombre": "Pocion Alucinogena",
            "tipo": "consumible",
            "cantidad": 2,
            "equipado": False,
        },
        {
            "id_item": 7,
            "nombre": "Collar Paralizante",
            "tipo": "equipable",
            "cantidad": 1,
            "equipado": False,
        },
        {
            "id_item": 8,
            "nombre": "Lanza Maldita",
            "tipo": "equipable",
            "cantidad": 1,
            "equipado": False,
        },
        {
            "id_item": 9,
            "nombre": "Espada de Doble Filo",
            "tipo": "equipable",
            "cantidad": 1,
            "equipado": False,
        },
        {
            "id_item": 10,
            "nombre": "Casco de Dullahan",
            "tipo": "equipable",
            "cantidad": 1,
            "equipado": True,
        },
        {
            "id_item": 11,
            "nombre": "Amuleto del Rey",
            "tipo": "clave",
            "cantidad": 1,
            "equipado": False,
        },
        {
            "id_item": 12,
            "nombre": "Pocion de Potencia",
            "tipo": "consumible",
            "cantidad": 4,
            "equipado": False,
        },
    ]

    for item in items_prueba:
        agregar_item(item, inv)

    manejar_inventario(inv)
