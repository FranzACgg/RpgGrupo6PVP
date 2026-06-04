from exploracion import manejar_exploracion
from combate import manejar_combate
from coliseo import manejar_coliseo
from cementerio import manejar_cementerio
from pantallas_finales import manejar_victoria, manejar_game_over
from estados import (
    SALIR,
    EXPLORACION,
    COMBATE,
    CEMENTERIO,
    COLISEO,
    GAME_OVER,
    VICTORIA,
)


def manejar_estados(contexto):
    while contexto["estado_actual"] != SALIR:
        if contexto["estado_actual"] == EXPLORACION:
            manejar_exploracion(contexto)
        elif contexto["estado_actual"] == COMBATE:
            manejar_combate(contexto)
        elif contexto["estado_actual"] == COLISEO:
            manejar_coliseo(contexto)
        elif contexto["estado_actual"] == CEMENTERIO:
            manejar_cementerio(contexto)
        elif contexto["estado_actual"] == GAME_OVER:
            manejar_game_over(contexto)
        elif contexto["estado_actual"] == VICTORIA:
            manejar_victoria(contexto)
