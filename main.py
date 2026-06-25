# main.py — Punto de entrada de GLASSTION

from menu_pre_final import menu_principal
from tutorial       import mostrar_tutorial
from personajes     import mostrar_seleccion_personaje, crear_personaje, PERSONAJES_SELECCIONABLES
from inventario     import crear_inventario, agregar_item
from main_mapas     import iniciar_mapas
from config         import crear_contexto
from estados        import EXPLORACION
from motor          import manejar_estados
from catalogo       import cargar_catalogo
from persistencia   import cargar_partida, cargar_progreso, guardar_progreso, borrar_partida


def finalizar_partida(contexto, progreso):
    """
    Entrada: Diccionario (contexto), Diccionario (progreso)
    Objetivo: cerrar la partida segun como termino. Si se gano el coliseo con
        las 3 vidas intactas, desbloquea la clase oculta y guarda el progreso.
        Si la partida termino (victoria o game over) borra el save para que no
        aparezca CONTINUAR de una partida ya terminada. Si se salio con Q, no
        toca nada (se puede continuar despues).
    Salida: none. Modifica progreso y los archivos de partida/progreso.
    """
    razon = contexto.get("razon_salida")
    if razon == "victoria":
        if contexto["personaje"]["vidas"] == 3:
            progreso["clase_oculta_desbloqueada"] = True
            guardar_progreso(progreso)
        borrar_partida()
    elif razon == "game_over":
        borrar_partida()


def iniciar_nueva_partida(progreso):
    """Crea un contexto nuevo: personaje, amuleto de resurrección y rivales del coliseo.
    Devuelve el contexto listo para jugar, o None si el jugador canceló."""
    contexto = crear_contexto()

    seleccion = mostrar_seleccion_personaje(progreso)
    if seleccion is None:
        return None

    personaje = crear_personaje(seleccion["nombre"], seleccion["clase"])
    if personaje is None:
        print("Error al crear el personaje.")
        return None

    contexto["personaje"]  = personaje
    contexto["inventario"] = crear_inventario()

    # Amuleto de Resurrección: vidas extra al inicio
    amuleto = {
        "id_item": 99, "nombre": "Amuleto de Resurrección",
        "tipo": "clave", "cantidad": 1, "equipado": True,
    }
    agregar_item(amuleto, contexto["inventario"])

    # Rivales del coliseo: los personajes que el jugador NO eligió
    rivales = [
        p for p in PERSONAJES_SELECCIONABLES
        if p["nombre"] != seleccion["nombre"] and not p["bloqueado"]
    ]
    contexto["progreso"]["rivales_coliseo"] = rivales
    contexto["progreso"]["rival_actual"]    = 0

    mostrar_tutorial()
    iniciar_mapas(contexto)
    contexto["estado_actual"] = EXPLORACION
    return contexto


def main():
    cargar_catalogo()
    progreso = cargar_progreso()

    accion = menu_principal()
    if accion == "salir":
        return

    if accion == "continuar":
        contexto = cargar_partida()
        if contexto is None:
            contexto = iniciar_nueva_partida(progreso)
    else:  # "nueva"
        contexto = iniciar_nueva_partida(progreso)

    if contexto is None:
        return

    manejar_estados(contexto)
    finalizar_partida(contexto, progreso)


if __name__ == "__main__":
    main()
