# Enemigos_dialogos - frases que dicen los enemigos durante el combate

# momentos del dialogo (que numero corresponde a cada situacion)
ENCUENTRO = 0   # cuando empieza la pelea
ATAQUE = 1      # cuando el enemigo ataca
DERROTA = 2     # cuando el enemigo es vencido

# frases por enemigo. la clave es el "tipo" que usa el juego (slime, goblin, jefe).
# cada enemigo tiene una tupla con 3 frases: (encuentro, ataque, derrota)
ENEMIGOS_DIALOGOS = {
    "slime": (
        "Glup...? Glup glup!",
        "Gloosh! Salpicon acido!",
        "Gluuu... me derrito...",
    ),
    "goblin": (
        "Jeje! Tu cabeza vale oro en el mercado!",
        "Mi daga rompe escudos, tonto!",
        "No... esta cueva era mia...",
    ),
    "jefe": (
        "Asi que vos sos el retador? Bienvenido al Coliseo.",
        "Senti la furia del Campeon!",
        "Imposible... un Campeon no cae asi...",
    ),
}


def obtener_dialogo(tipo, momento):
    # devuelve la frase del enemigo segun el momento. si no tiene, devuelve ""
    tipo = tipo.lower()   # por si viene "Slime" en vez de "slime"
    if tipo not in ENEMIGOS_DIALOGOS:
        return ""
    frases = ENEMIGOS_DIALOGOS[tipo]
    return frases[momento]


def dialogo_de_enemigo(enemigo, momento):
    # recibe un enemigo del juego (diccionario con la clave "tipo") y devuelve su frase
    return obtener_dialogo(enemigo["tipo"], momento)
