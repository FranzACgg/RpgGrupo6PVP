# Momentos del dialogo. Usamos numeros con nombre para que se entienda mejor
ENCUENTRO = 0  # cuando aparece el enemigo
ATAQUE = 1     # cuando el enemigo ataca
DERROTA = 2    # cuando el enemigo es vencido

# diccionario con los dialogos de cada enemigo
# La clave es el tipo de enemigo y el valor es una tupla con 3 frases:
# (frase de encuentro, frase de ataque, frase de derrota)
ENEMIGOS_DIALOGOS = {
    "slime": (
        "Glup...? Glup glup!",
        "Gloosh! Gloosh!",
        "Gluuu... plop...",
    ),
    "guerrero": (
        "Solo uno puede ser rey, y no vas a ser vos.",
        "Senti el peso de mi espada!",
        "Imposible... mi escudo no alcanzo...",
    ),
    "pirata": (
        "Je! Otro tonto que quiere quitarme el tesoro?",
        "Toma esto, rata de tierra firme!",
        "Maldicion... me hundo como un barco viejo...",
    ),
    "bufon": (
        "Jaja! Viniste a jugar conmigo?",
        "A ver si adivinas de donde viene el golpe!",
        "Mi mejor truco... y aun asi perdi...",
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
