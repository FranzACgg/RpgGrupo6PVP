import os
import msvcrt
from inventario import agregar_item, busqueda_item_por_id, descartar_item

NOMBRE_MERCADER = "Mercader del Cementerio"

TEXTOS_MERCADER = {
    "saludo": "Si encontras tesoros cavando por ahi, traelos. Te doy buen oro.",
    "despedida": "Suerte ahi afuera, la vas a necesitar.",
}

ID_ORO = 100


def cargar_tienda():
    # leemos la tienda del archivo tienda.txt. cada linea es: id;nombre;tipo;precio
    articulos = []
    try:
        ruta_actual = os.path.dirname(__file__)              # carpeta de este archivo
        ruta_archivo = os.path.join(ruta_actual, "tienda.txt")
        with open(ruta_archivo, "rt") as archivo:
            for linea in archivo:
                if linea.strip() == "":
                    continue
                # desempaquetamos los campos separados por ;
                id_item, nombre, tipo_item, precio = linea.strip().split(";")
                item = {
                    "id_item": int(id_item),
                    "nombre": nombre,
                    "tipo": tipo_item,
                    "cantidad": 1,
                    "equipado": False,
                }
                articulos.append({"item": item, "precio": int(precio)})
    except Exception as e:
        print("Error", e)
    return articulos


def cantidad_de_oro(inventario):
    # el oro lo guardamos como un item mas del inventario (id ID_ORO)
    i = busqueda_item_por_id(ID_ORO, inventario)
    if i == -1:
        return 0
    else:
        return inventario[i]["cantidad"]


def sumar_oro(inventario, cantidad):
    # suma oro; si todavia no hay item de oro, lo crea
    i = busqueda_item_por_id(ID_ORO, inventario)
    if i == -1:
        inventario.append({"id_item": ID_ORO, "nombre": "Oro", "tipo": "clave", "cantidad": cantidad, "equipado": False})
    else:
        inventario[i]["cantidad"] += cantidad


def restar_oro(inventario, cantidad):
    # resta oro
    i = busqueda_item_por_id(ID_ORO, inventario)
    if i != -1:
        inventario[i]["cantidad"] -= cantidad


def precio_de_venta(id_item, articulos):
    # el mercader compra a la mitad del precio; si no lo vende, paga 5
    for articulo in articulos:
        if articulo["item"]["id_item"] == id_item:
            return articulo["precio"] // 2
    return 5


def limpiar_pantalla():
    # limpia la consola (os.system no es de clase; va para que el menu se vea prolijo)
    os.system("cls" if os.name == "nt" else "clear")


def leer_tecla():
    # lee una tecla sin apretar enter (no es de clase). sirve para moverse por el menu
    return msvcrt.getch().decode("utf-8", errors="ignore").lower()


def menu_comprar(inventario, articulos):
    cursor = 0       # opcion marcada con ">"
    mensaje = ""

    while True:
        limpiar_pantalla()
        print("===  COMPRAR  ===")
        print(f"Tu oro: {cantidad_de_oro(inventario)}")
        print("-" * 40)

        if len(articulos) == 0:
            print("El mercader no tiene nada para vender.")
        else:
            # mostramos cada objeto; el marcado lleva ">"
            for i in range(len(articulos)):
                nombre = articulos[i]["item"]["nombre"]
                precio = articulos[i]["precio"]
                if i == cursor:
                    marca = ">"
                else:
                    marca = " "
                print(f"{marca} {nombre} - {precio} oro")

        print("-" * 40)
        if mensaje != "":
            print(mensaje)
            print("-" * 40)
        print("W/S: mover   E: comprar   Q: volver")

        tecla = leer_tecla()
        if tecla == "q":
            return
        elif tecla == "w":
            if cursor > 0:
                cursor -= 1
        elif tecla == "s":
            if cursor < len(articulos) - 1:
                cursor += 1
        elif tecla == "e":
            if len(articulos) > 0:
                precio = articulos[cursor]["precio"]
                item = articulos[cursor]["item"]
                if cantidad_de_oro(inventario) >= precio:
                    # agregar_item es del equipo: da False si el inventario esta lleno
                    if agregar_item(item, inventario):
                        restar_oro(inventario, precio)
                        mensaje = f"Compraste {item['nombre']}."
                    else:
                        mensaje = "Tu inventario esta lleno."
                else:
                    mensaje = "No te alcanza el oro."


def menu_vender(inventario, articulos):
    cursor = 0
    mensaje = ""

    while True:
        # vendible: todo menos el oro, los "clave" (pala/quests) y lo equipado
        vendibles = []
        for item in inventario:
            if item["id_item"] != ID_ORO and item["tipo"] != "clave" and not item["equipado"]:
                vendibles.append(item)

        # si vendiste el ultimo, acomodamos el cursor
        if cursor >= len(vendibles):
            cursor = len(vendibles) - 1
        if cursor < 0:
            cursor = 0

        limpiar_pantalla()
        print("===  VENDER  ===")
        print(f"Tu oro: {cantidad_de_oro(inventario)}")
        print("-" * 40)

        if len(vendibles) == 0:
            print("No tenes nada para vender.")
        else:
            for i in range(len(vendibles)):
                nombre = vendibles[i]["nombre"]
                cantidad = vendibles[i]["cantidad"]
                precio = precio_de_venta(vendibles[i]["id_item"], articulos)
                if i == cursor:
                    marca = ">"
                else:
                    marca = " "
                print(f"{marca} {nombre} x{cantidad} - {precio} oro")

        print("-" * 40)
        if mensaje != "":
            print(mensaje)
            print("-" * 40)
        print("W/S: mover   E: vender   Q: volver")

        tecla = leer_tecla()
        if tecla == "q":
            return
        elif tecla == "w":
            if cursor > 0:
                cursor -= 1
        elif tecla == "s":
            if cursor < len(vendibles) - 1:
                cursor += 1
        elif tecla == "e":
            if len(vendibles) > 0:
                item = vendibles[cursor]
                precio = precio_de_venta(item["id_item"], articulos)
                # descartar_item es del equipo: saca una unidad y da True si pudo
                if descartar_item(item["id_item"], inventario):
                    sumar_oro(inventario, precio)
                    mensaje = f"Vendiste {item['nombre']} por {precio} oro."


def conversar_con_comerciante(inventario):
    # funcion principal: la llama el juego pasando el inventario del jugador
    articulos = cargar_tienda()   # leemos la tienda del archivo al entrar
    opciones = ("Comprar", "Vender", "Salir")
    cursor = 0

    while True:
        limpiar_pantalla()
        print(f"===  {NOMBRE_MERCADER}  ===")
        print()
        print(f"{NOMBRE_MERCADER}: {TEXTOS_MERCADER['saludo']}")
        print(f"Tu oro: {cantidad_de_oro(inventario)}")
        print("-" * 40)

        for i in range(len(opciones)):
            if i == cursor:
                marca = ">"
            else:
                marca = " "
            print(f"{marca} {opciones[i]}")

        print("-" * 40)
        print("W/S: mover   E: elegir   Q: salir")

        tecla = leer_tecla()
        if tecla == "w":
            if cursor > 0:
                cursor -= 1
        elif tecla == "s":
            if cursor < len(opciones) - 1:
                cursor += 1
        elif tecla == "e":
            # segun la opcion marcada: comprar, vender o salir
            if cursor == 0:
                menu_comprar(inventario, articulos)
            elif cursor == 1:
                menu_vender(inventario, articulos)
            elif cursor == 2:
                despedirse()
                return
        elif tecla == "q":
            despedirse()
            return


def despedirse():
    # frase de despedida antes de volver al juego
    limpiar_pantalla()
    print(f"{NOMBRE_MERCADER}: {TEXTOS_MERCADER['despedida']}")
    print()
    print("Presiona cualquier tecla para volver...")
    leer_tecla()
