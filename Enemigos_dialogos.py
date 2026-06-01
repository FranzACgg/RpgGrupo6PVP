# Momentos del dialogo. Usamos numeros con nombre para que se entienda mejor
ENCUENTRO = 0  # cuando aparece el enemigo
ATAQUE = 1     # cuando el enemigo ataca
DERROTA = 2    # cuando el enemigo es vencido

# DICCIONARIO con los dialogos de cada enemigo
# La clave es el tipo de enemigo y el valor es una tupla con 3 frases:
# (frase de encuentro, frase de ataque, frase de derrota)
ENEMIGOS_DIALOGOS = {
    "slime": (
        "Un slime tembloroso te bloquea el camino.",
        "El slime salta y te embiste!",
        "El slime se deshace en un charco.",
    ),
    "guerrero": (
        "Un guerrero rival levanta su escudo frente a vos.",
        "El guerrero descarga un golpe brutal!",
        "El guerrero cae de rodillas, vencido.",
    ),
    "pirata": (
        "Un pirata te apunta con su mosquete.",
        "El pirata dispara sin piedad!",
        "El pirata suelta su espada y se rinde.",
    ),
    "bufon": (
        "Un bufon rie mientras te rodea.",
        "El bufon te arroja un cuchillo!",
        "El bufon hace una ultima reverencia y cae.",
    ),
}


def mostrar_dialogo(tipo, momento):
    # Muestra una frase del enemigo segun el momento (encuentro, ataque o derrota)
    if tipo not in ENEMIGOS_DIALOGOS:
        print("Ese enemigo no tiene dialogos.")
        return
    frases = ENEMIGOS_DIALOGOS[tipo]
    print(frases[momento])


# Punto de inicio para probar la base de dialogos solo
if __name__ == "__main__":
    # Recorremos todos los enemigos y mostramos sus 3 frases
    for tipo in ENEMIGOS_DIALOGOS:
        print("=== " + tipo + " ===")
        mostrar_dialogo(tipo, ENCUENTRO)
        mostrar_dialogo(tipo, ATAQUE)
        mostrar_dialogo(tipo, DERROTA)
        print()
