import random
import os
import msvcrt


CLASES_DISPONIBLES = {
    "Guerrero": {
        "stats_base": {
            "fuerza": 80,
            "defensa": 70,
            "magia": 10,
            "espiritu": 20,
            "agilidad": 40,
            "suerte": 0,
            "hp": 200,
            "mp": 30,
        },
        "habilidades": [
            {
                "nombre": "Golpe Brutal",
                "tipo": "fisico",
                "valor": 35,
                "probabilidad": 90,
                "costo_mp": 5,
            },
            {
                "nombre": "Escudo de Acero",
                "tipo": "fisico",
                "valor": 20,
                "probabilidad": 80,
                "costo_mp": 8,
            },
            {
                "nombre": "Grito de Guerra",
                "tipo": "fisico",
                "valor": 50,
                "probabilidad": 60,
                "costo_mp": 15,
            },
        ],
    },
    "Pirata": {
        "stats_base": {
            "fuerza": 200,
            "defensa": 40,
            "magia": 15,
            "espiritu": 25,
            "agilidad": 60,
            "suerte": 0,
            "hp": 100,
            "mp": 80,
        },
        "habilidades": [
            {
                "nombre": "Espadazo Pirata",
                "tipo": "fisico",
                "valor": 40,
                "probabilidad": 85,
                "costo_mp": 5,
            },
            {
                "nombre": "Disparo de Mosquete",
                "tipo": "fisico",
                "valor": 55,
                "probabilidad": 70,
                "costo_mp": 10,
            },
            {
                "nombre": "Maldicion del Mar",
                "tipo": "magico",
                "valor": 45,
                "probabilidad": 65,
                "costo_mp": 20,
            },
        ],
    },
    "Bufon": {
        "stats_base": {
            "fuerza": 80,
            "defensa": 25,
            "magia": 55,
            "espiritu": 35,
            "agilidad": 90,
            "suerte": 0,
            "hp": 90,
            "mp": 70,
        },
        "habilidades": [
            {
                "nombre": "Cuchillo Arrojadizo",
                "tipo": "fisico",
                "valor": 25,
                "probabilidad": 92,
                "costo_mp": 3,
            },
            {
                "nombre": "Confusion Magica",
                "tipo": "magico",
                "valor": 50,
                "probabilidad": 55,
                "costo_mp": 25,
            },
            {
                "nombre": "Bofeton Humillante",
                "tipo": "fisico",
                "valor": 15,
                "probabilidad": 98,
                "costo_mp": 0,
            },
        ],
    },
}

PERSONAJES_SELECCIONABLES = [
    {
        "nombre": "Ragnar",
        "clase": "Guerrero",
        "descripcion": "Un guerrero resistente con gran defensa y mucha vida.",
        "bloqueado": False,
    },
    {
        "nombre": "Morgan",
        "clase": "Pirata",
        "descripcion": "Un combatiente agresivo con gran fuerza y ataques impredecibles.",
        "bloqueado": False,
    },
    {
        "nombre": "Loki",
        "clase": "Bufon",
        "descripcion": "Rápido, escurridizo y experto en trucos y magia.",
        "bloqueado": False,
    },
    {
        "nombre": "???",
        "clase": "Oculto",
        "descripcion": "Este personaje aún no ha sido descubierto.",
        "bloqueado": True,
    },
]


def crear_personaje(nombre, clase):
    if clase not in CLASES_DISPONIBLES:
        return None

    datos_clase = CLASES_DISPONIBLES[clase]
    stats = datos_clase["stats_base"].copy()

    habilidades = []
    for habilidad in datos_clase["habilidades"]:
        habilidades.append(habilidad.copy())

    personaje = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "vidas": 3,
        "stats_base": stats,
        "stats_actuales": {
            "hp": stats["hp"],
            "mp": stats["mp"],
        },
        "habilidades": habilidades,
    }
    return personaje


def recibir_danio(personaje, cantidad, tipo):
    if tipo == "fisico":
        danio_final = cantidad - personaje["stats_base"]["defensa"]
    elif tipo == "magico":
        danio_final = cantidad - personaje["stats_base"]["espiritu"]
    else:
        danio_final = cantidad

    if danio_final < 1:
        danio_final = 1

    personaje["stats_actuales"]["hp"] -= danio_final
    if personaje["stats_actuales"]["hp"] < 0:
        personaje["stats_actuales"]["hp"] = 0

    return danio_final


def curar(personaje, cantidad):
    hp_max = personaje["stats_base"]["hp"]
    hp_actual = personaje["stats_actuales"]["hp"]
    espacio = hp_max - hp_actual
    curado = min(cantidad, espacio)
    personaje["stats_actuales"]["hp"] += curado
    return curado


def esta_vivo(personaje):
    return personaje["stats_actuales"]["hp"] > 0


def usar_habilidad(personaje, indice_habilidad):
    habilidades = personaje["habilidades"]
    if indice_habilidad < 0 or indice_habilidad >= len(habilidades):
        return None

    habilidad = habilidades[indice_habilidad]
    if personaje["stats_actuales"]["mp"] < habilidad["costo_mp"]:
        return None

    personaje["stats_actuales"]["mp"] -= habilidad["costo_mp"]
    tirada = random.randint(1, 100)
    exito = tirada <= habilidad["probabilidad"]

    return {"exito": exito, "habilidad": habilidad}


def revivir(personaje):
    if personaje["vidas"] <= 0:
        return False
    personaje["vidas"] -= 1
    personaje["stats_actuales"]["hp"] = personaje["stats_base"]["hp"]
    personaje["stats_actuales"]["mp"] = personaje["stats_base"]["mp"]
    return True


def aplicar_efecto_consumible(personaje, item):
    if item["tipo"] != "consumible":
        return None

    efecto = item.get("efecto", {})
    if "hp" in efecto:
        curar(personaje, efecto["hp"])
    if "mp" in efecto:
        mp_max = personaje["stats_base"]["mp"]
        personaje["stats_actuales"]["mp"] = min(
            personaje["stats_actuales"]["mp"] + efecto["mp"], mp_max
        )
    return item


def obtener_stats_con_equipamiento(personaje, items_equipados):
    stats_totales = personaje["stats_base"].copy()
    for item in items_equipados:
        efecto = item.get("efecto", {})
        for stat, valor in efecto.items():
            if stat in stats_totales:
                stats_totales[stat] += valor
    return stats_totales


def mostrar_stats(personaje):
    ancho = 36
    linea = "═" * ancho
    print(f"╔{linea}╗")
    print(
        f"║  {personaje['nombre']} ({personaje['clase']})".ljust(ancho + 2)
        + "║"
    )
    print(f"╠{linea}╣")
    print(
        f"║  Nivel : {personaje['nivel']}   Vidas: {'♥ ' * personaje['vidas']}".ljust(
            ancho + 2
        )
        + "║"
    )
    hp_a = personaje["stats_actuales"]["hp"]
    hp_m = personaje["stats_base"]["hp"]
    mp_a = personaje["stats_actuales"]["mp"]
    mp_m = personaje["stats_base"]["mp"]
    print(f"║  HP : {hp_a:>3} / {hp_m:<3}   MP : {mp_a:>3} / {mp_m:<3}  ║")
    print(f"╠{linea}╣")
    sb = personaje["stats_base"]
    stats_mostrar = [
        "fuerza",
        "defensa",
        "magia",
        "espiritu",
        "agilidad",
        "suerte",
    ]
    for stat in stats_mostrar:
        linea_stat = f"║  {stat.capitalize():<10}: {sb[stat]:<4}"
        print(linea_stat.ljust(ancho + 2) + "║")
    print(f"╚{linea}╝")


def mostrar_seleccion_personaje():
    cursor = 0

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("╔════════════════════════════════════════════════════╗")
        print("║             SELECCIÓN DE PERSONAJE                 ║")
        print("╠════════════════════════════════════════════════════╣")

        for i, personaje in enumerate(PERSONAJES_SELECCIONABLES):
            marcador = "►" if i == cursor else " "
            texto = f"{marcador} {personaje['nombre']} - {personaje['clase']}"
            print(f"║ {texto}".ljust(53) + "║")

        print("╠════════════════════════════════════════════════════╣")

        personaje_actual = PERSONAJES_SELECCIONABLES[cursor]

        if personaje_actual["bloqueado"]:
            print("║ Nombre: ???".ljust(53) + "║")
            print("║ Clase : ???".ljust(53) + "║")
            print("║ Este personaje permanece oculto...".ljust(53) + "║")
            print("╠════════════════════════════════════════════════════╣")
            print("║ HP:???  MP:???  FUE:???  DEF:???".ljust(53) + "║")
            print("║ MAG:???  ESP:???  AGI:???  SUE:???".ljust(53) + "║")
            print("╠════════════════════════════════════════════════════╣")
            print("║ Habilidades:".ljust(53) + "║")
            print("║ - ???".ljust(53) + "║")
            print("║ - ???".ljust(53) + "║")
            print("║ - ???".ljust(53) + "║")
        else:
            clase_actual = personaje_actual["clase"]
            datos = CLASES_DISPONIBLES[clase_actual]
            sb = datos["stats_base"]

            descripcion = personaje_actual["descripcion"]
            if len(descripcion) > 50:
                descripcion = descripcion[:47] + "..."

            print(f"║ Nombre: {personaje_actual['nombre']}".ljust(53) + "║")
            print(f"║ Clase : {clase_actual}".ljust(53) + "║")
            print(f"║ {descripcion}".ljust(53) + "║")
            print("╠════════════════════════════════════════════════════╣")
            print(
                f"║ HP:{sb['hp']}  MP:{sb['mp']}  FUE:{sb['fuerza']}  DEF:{sb['defensa']}".ljust(
                    53
                )
                + "║"
            )
            print(
                f"║ MAG:{sb['magia']}  ESP:{sb['espiritu']}  AGI:{sb['agilidad']}  SUE:{sb['suerte']}".ljust(
                    53
                )
                + "║"
            )
            print("╠════════════════════════════════════════════════════╣")
            print("║ Habilidades:".ljust(53) + "║")

            for hab in datos["habilidades"]:
                linea_hab = f"- {hab['nombre']} | MP:{hab['costo_mp']} | %:{hab['probabilidad']}"
                print(f"║ {linea_hab}".ljust(53) + "║")

        print("╠════════════════════════════════════════════════════╣")
        print("║ W/S: mover   E: seleccionar".ljust(53) + "║")
        print("╚════════════════════════════════════════════════════╝")

        tecla = msvcrt.getch().decode("utf-8", errors="ignore").lower()

        if tecla == "w":
            cursor = (cursor - 1) % len(PERSONAJES_SELECCIONABLES)
        elif tecla == "s":
            cursor = (cursor + 1) % len(PERSONAJES_SELECCIONABLES)
        elif tecla == "e":
            if personaje_actual["bloqueado"]:
                os.system("cls" if os.name == "nt" else "clear")
                print("╔══════════════════════════════════════╗")
                print("║      PERSONAJE AÚN BLOQUEADO         ║")
                print("║   Debes cumplir una condición para   ║")
                print("║         poder desbloquearlo.         ║")
                print("╚══════════════════════════════════════╝")
                print("\nPresiona cualquier tecla para continuar...")
                msvcrt.getch()
            else:
                return personaje_actual


def menu_personaje(personaje):
    pestanas = ["INFO", "STATS", "HABILIDADES"]
    tab = 0
    ancho = 40

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        encabezado = f"  {personaje['nombre']}  —  {personaje['clase']}"
        print("╔" + "═" * ancho + "╗")
        print("║" + encabezado.ljust(ancho) + "║")

        barra_tabs = "  "
        for i, p in enumerate(pestanas):
            if i == tab:
                barra_tabs += f"[{p}]"
            else:
                barra_tabs += f" {p} "
        print("╠" + "═" * ancho + "╣")
        print("║" + barra_tabs.ljust(ancho) + "║")
        print("╠" + "═" * ancho + "╣")

        if tab == 0:
            hp_a = personaje["stats_actuales"]["hp"]
            hp_m = personaje["stats_base"]["hp"]
            mp_a = personaje["stats_actuales"]["mp"]
            mp_m = personaje["stats_base"]["mp"]
            vidas_str = "♥ " * personaje["vidas"] + "♡ " * (
                3 - personaje["vidas"]
            )
            filas = [
                f"  Nivel   : {personaje['nivel']}",
                f"  Vidas   : {vidas_str}",
                f"  HP      : {hp_a} / {hp_m}",
                f"  MP      : {mp_a} / {mp_m}",
            ]
            for fila in filas:
                print("║" + fila.ljust(ancho) + "║")
            for _ in range(4):
                print("║" + " " * ancho + "║")

        elif tab == 1:
            sb = personaje["stats_base"]
            stats = [
                "fuerza",
                "defensa",
                "magia",
                "espiritu",
                "agilidad",
                "suerte",
            ]
            for stat in stats:
                barras = "█" * (sb[stat] // 10) + "░" * (10 - sb[stat] // 10)
                fila = f"  {stat.capitalize():<10}: {sb[stat]:<3}  {barras}"
                print("║" + fila.ljust(ancho) + "║")
            for _ in range(2):
                print("║" + " " * ancho + "║")

        elif tab == 2:
            for hab in personaje["habilidades"]:
                nombre = f"  ► {hab['nombre']}"
                print("║" + nombre.ljust(ancho) + "║")
                detalle = f"    {hab['tipo'].capitalize()}  |  Valor: {hab['valor']}  |  MP: {hab['costo_mp']}  |  %{hab['probabilidad']}"
                print("║" + detalle.ljust(ancho) + "║")
            for _ in range(2):
                print("║" + " " * ancho + "║")

        print("╠" + "═" * ancho + "╣")
        print("║" + "  A/D: cambiar pestaña   Q: Volver".ljust(ancho) + "║")
        print("╚" + "═" * ancho + "╝")

        tecla = msvcrt.getch().decode("utf-8", errors="ignore").lower()
        if tecla == "a":
            tab = (tab - 1) % len(pestanas)
        elif tecla == "d":
            tab = (tab + 1) % len(pestanas)
        elif tecla == "q":
            break


if __name__ == "__main__":
    while True:
        seleccion = mostrar_seleccion_personaje()
        personaje = crear_personaje(seleccion["nombre"], seleccion["clase"])

        if personaje is not None:
            menu_personaje(personaje)
        else:
            print("Error al crear el personaje.")
            break
