# main.py — Punto de entrada de GLASSTION
# Flujo: Menú principal → Selección de personaje → Juego

from menu_pre_final import menu_principal
from personajes import mostrar_seleccion_personaje, crear_personaje
from inventario import crear_inventario
from main_mapas import iniciar_mapas, iniciar_mapa
from config import estado, crear_contexto

contexto = crear_contexto()


def main():
    # ── 1. Menú principal ─────────────────────────────────────────────────────
    accion = menu_principal()
    if accion != "empezar":
        return  # El jugador eligió Salir

    # ── 2. Selección de personaje ─────────────────────────────────────────────
    seleccion = mostrar_seleccion_personaje()
    if seleccion is None:
        return

    personaje = crear_personaje(seleccion["nombre"], seleccion["clase"])
    if personaje is None:
        print("Error al crear el personaje.")
        return

    # ── 3. Cargar personaje en el estado global ───────────────────────────────
    estado["personaje"] = personaje
    estado["hp"] = personaje["stats_actuales"]["hp"]
    estado["mp"] = personaje["stats_actuales"]["mp"]
    estado["hp_max"] = personaje["stats_base"]["hp"]
    estado["mp_max"] = personaje["stats_base"]["mp"]
    estado["inventario"] = crear_inventario()

    # ── 4. Generar mapa inicial y arrancar ────────────────────────────────────
    iniciar_mapas(contexto)  # configura estado["mapa_actual"] con el Prado
    iniciar_mapa()  # bucle principal — no retorna salvo exit()


if __name__ == "__main__":
    main()
