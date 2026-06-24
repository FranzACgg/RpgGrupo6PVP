# main.py — Punto de entrada de GLASSTION

from menu_pre_final import menu_principal
from personajes import mostrar_seleccion_personaje, crear_personaje
from inventario import crear_inventario
from main_mapas import iniciar_mapas
from config import crear_contexto
from estados import EXPLORACION
from motor import manejar_estados
from catalogo import cargar_catalogo
from persistencia import cargar_partida, cargar_progreso


def iniciar_nueva_partida():
    """Crea un contexto nuevo con el personaje elegido.
    Devuelve el contexto listo para jugar, o None si el jugador canceló."""
    contexto = crear_contexto()

    seleccion = mostrar_seleccion_personaje()
    if seleccion is None:
        return None

    personaje = crear_personaje(seleccion["nombre"], seleccion["clase"])
    if personaje is None:
        print("Error al crear el personaje.")
        return None

    contexto["personaje"] = personaje
    contexto["inventario"] = crear_inventario()
    iniciar_mapas(contexto)
    contexto["estado_actual"] = EXPLORACION
    return contexto


def main():
    cargar_catalogo()
    progreso = (
        cargar_progreso()
    )  # TODO: usar para mostrar/ocultar la 4ª clase en selección

    accion = menu_principal()

    if accion == "salir":
        return

    if accion == "continuar":
        contexto = cargar_partida()
        if contexto is None:
            # El save no estaba o estaba corrupto → arrancamos una nueva
            contexto = iniciar_nueva_partida()
    else:  # "nueva"
        contexto = iniciar_nueva_partida()

    if contexto is None:
        return

    manejar_estados(contexto)


if __name__ == "__main__":
    main()
