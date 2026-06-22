# main.py — Punto de entrada de GLASSTION
# Flujo: Menú principal → Selección de personaje → Juego

from menu_pre_final import menu_principal
from personajes import mostrar_seleccion_personaje, crear_personaje
from inventario import crear_inventario
from main_mapas import iniciar_mapas
from config import crear_contexto
from estados import EXPLORACION
from motor import manejar_estados
from catalogo import cargar_catalogo


def main():
    # ── 1. Crear contexto ─────────────────────────────────────────────────────
    contexto = crear_contexto()
    cargar_catalogo()

    # ── 2. Menú principal ─────────────────────────────────────────────────────
    accion = menu_principal()
    if accion != "empezar":
        return  # El jugador eligió Salir

    # ── 3. Selección de personaje ─────────────────────────────────────────────
    seleccion = mostrar_seleccion_personaje()
    if seleccion is None:
        return

    personaje = crear_personaje(seleccion["nombre"], seleccion["clase"])
    if personaje is None:
        print("Error al crear el personaje.")
        return

    # ── 4. Cargar personaje en el contexto ───────────────────────────────
    contexto["personaje"] = personaje
    contexto["inventario"] = crear_inventario()

    # ── 5. Generar mapa inicial y arrancar ────────────────────────────────────
    iniciar_mapas(contexto)
    contexto["estado_actual"] = EXPLORACION
    manejar_estados(contexto)  # bucle principal


if __name__ == "__main__":
    main()
