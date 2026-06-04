from estados import EXPLORACION
from entidades import mover_slimes
from ui import dibujar_juego_centrado
from jugador import cambio_de_mapa
from main_mapas import (
    obtener_tecla,
    procesar_entrada,
)

# TODO(diseño): procesar_entrada es específico de exploración; mover acá cuando combate haga el suyo


def manejar_exploracion(contexto):
    contexto["estado_actual"] = EXPLORACION
    while contexto["estado_actual"] == EXPLORACION:
        dibujar_juego_centrado(contexto)

        tecla = obtener_tecla()
        procesar_entrada(tecla, contexto)

        # Slimes solo se mueven en el Prado (mapa 2)
        if contexto["mundo"]["numero_mapa"] == 2:
            contexto["mundo"]["pasos_jugador"] += 1
            if contexto["mundo"]["pasos_jugador"] % 2 == 0:
                mover_slimes(contexto["mundo"]["mapa_actual"], contexto)

        cambio_de_mapa(contexto)
