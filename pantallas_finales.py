from estados import VICTORIA, GAME_OVER


def manejar_victoria(contexto):
    contexto["estado_actual"] = VICTORIA


def manejar_game_over(contexto):
    contexto["estado_actual"] = GAME_OVER
