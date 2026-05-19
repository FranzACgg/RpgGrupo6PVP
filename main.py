"""
main.py

Archivo orquestador para integrar los módulos del proyecto RPG.

OJO:
Este archivo asume que renombraste los módulos a nombres importables,
por ejemplo:
- MENU PRE-FINAL.py      -> menu_pre_final.py
- personaje (2).py       -> personaje.py
- tresMapas_unidos (1).py-> tresMapas_unidos.py
- Inventario.py          -> Inventario.py

Además, asume estos ajustes mínimos:
1) menu_principal() devuelve "empezar" o "salir".
2) iniciar_mapa(...) NO se ejecuta solo al importar el módulo.
3) iniciar_mapa(...) acepta personaje, inventario y una función para abrir inventario.
"""

from menu_pre_final import menu_principal
from personajes import mostrar_seleccion_personaje, crear_personaje
from inventario import crear_inventario, manejar_inventario
from main_mapas import iniciar_mapas, iniciar_mapa


def main():
    # 1) Menú principal
    accion = menu_principal()
    if accion != 'empezar':
        return

    # 2) Selección y creación de personaje
    seleccion = mostrar_seleccion_personaje()
    if seleccion is None:
        return

    personaje = crear_personaje(seleccion['nombre'], seleccion['clase'])
    if personaje is None:
        print('Error al crear el personaje.')
        return

    # 3) Crear inventario
    inventario = crear_inventario()

    # 4) Crear mapa inicial
    mapa_inicial = iniciar_mapas()
    numero_mapa_inicial = 2  # 2 = prado, según tu módulo de mapas

    # 5) Entrar al mapa
    iniciar_mapa(
        mapa_inicial,
        numero_mapa_inicial,
        inventario,
    )


if __name__ == '__main__':
    main()
