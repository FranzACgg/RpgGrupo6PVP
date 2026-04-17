# Para subir cambios a github
# git push origin Personajes y stats

# para descargar los cambios de otros
# git fetch origin -a
# git pull origin main

# para guardar cambios localmente
# git add personajes_stats.py
# git commit -m "comentario"


# funcion def para crear personajes con nombres de mitologia nordica juego rpg usando diccionarios. 
# agrega un docstring a la funcion con entrada, salida y objetivo de la funcion

def crear_personaje(nombre, clase):
    stats = asignar_stats_por_clase(clase)

    if stats is None:
        return None

    personaje = {
        "nombre": nombre,
        "clase": clase,
        "vida_actual": stats["vida_max"],
        "vida_max": stats["vida_max"],
        "mana": stats["mana"],
        "estado": "vivo",
        "estadisticas": {
            "fuerza": stats["fuerza"],
            "defensa": stats["defensa"],
            "velocidad": stats["velocidad"],
            "critico": stats["critico"]
        }
    }

    return personaje


# funcion def para asignar estadisticas a los personajes creados con la funcion anterior, utilizando diccionarios anidados. 
# agrega un docstring a la funcion con entrada, salida y objetivo de la funcion

def asignar_stats_por_clase(clase):
    if clase == "Guerrero":
        return {
            "vida_max": 120,
            "mana": 30,
            "fuerza": 15,
            "defensa": 10,
            "velocidad": 5,
            "critico": 10
        }

    elif clase == "Mago":
        return {
            "vida_max": 80,
            "mana": 100,
            "fuerza": 20,
            "defensa": 3,
            "velocidad": 6,
            "critico": 15
        }

    elif clase == "Arquera":
        return {
            "vida_max": 90,
            "mana": 50,
            "fuerza": 12,
            "defensa": 5,
            "velocidad": 12,
            "critico": 25
        }

    else:
        print("Clase no válida")
        return None


personaje1 = crear_personaje("Ragnar", "Guerrero")
personaje2 = crear_personaje("Eldrion", "Mago")
personaje3 = crear_personaje("Mirella", "Arquera")

#Funcion para recibir daño a un personaje y actualizar su vida actual, si la vida llega a 0 o menos, cambiar el estado a "muerto". 
# Agrega un docstring a la funcion con entrada, salida y objetivo de la funcion

def recibir_danio_con_defensa(personaje, dano, defensa_total):
    dano_final = dano - defensa_total

    if dano_final < 0:
        dano_final = 0

    personaje["vida_actual"] -= dano_final

    if personaje["vida_actual"] <= 0:
        personaje["vida_actual"] = 0
        personaje["estado"] = "muerto"

    return dano_final

def curar(personaje, cantidad):
    if personaje["estado"] == "muerto":
        print("No se puede curar un personaje muerto")
        return
    
    personaje["vida_actual"] += cantidad
    
    # No puede superar la vida máxima
    if personaje["vida_actual"] > personaje["vida_max"]:
        personaje["vida_actual"] = personaje["vida_max"]
    
    print(f"{personaje['nombre']} se cura {cantidad} de vida")

def esta_vivo(personaje):
    return personaje["estado"] == "vivo"

#Funcion para el combate entre dos personajes, donde cada uno ataca al otro y se actualizan sus vidas y estados.

import random

import random

def atacar(atacante, defensor, equipo_atacante=None, equipo_defensor=None):
    stats_atacante = obtener_stats_combate(atacante, equipo_atacante)
    stats_defensor = obtener_stats_combate(defensor, equipo_defensor)

    dano_base = stats_atacante["fuerza"]
    prob_critico = stats_atacante["critico"]

    es_critico = random.randint(1, 100) <= prob_critico

    if es_critico:
        dano_base *= 2

    dano_real = recibir_danio_con_defensa(defensor, dano_base, stats_defensor["defensa"])

    resultado = {
        "atacante": atacante["nombre"],
        "defensor": defensor["nombre"],
        "critico": es_critico,
        "dano_base": dano_base,
        "dano_real": dano_real,
        "vida_restante": defensor["vida_actual"],
        "defensor_sigue_vivo": esta_vivo(defensor),
        "stats_atacante": stats_atacante,
        "stats_defensor": stats_defensor
    }

    return resultado


def combate_simple(personaje1, personaje2):
    turno = 1

    while esta_vivo(personaje1) and esta_vivo(personaje2):
        print(f"\n--- Turno {turno} ---")

        resultado1 = atacar(personaje1, personaje2)
        print(f"{resultado1['atacante']} ataca a {resultado1['defensor']}")

        if resultado1["critico"]:
            print("¡Golpe crítico!")

        print(f"Daño real: {resultado1['dano_real']}")
        print(f"Vida restante de {resultado1['defensor']}: {resultado1['vida_restante']}")

        if not resultado1["defensor_sigue_vivo"]:
            print(f"{personaje2['nombre']} ha sido derrotado")
            break

        resultado2 = atacar(personaje2, personaje1)
        print(f"{resultado2['atacante']} ataca a {resultado2['defensor']}")

        if resultado2["critico"]:
            print("¡Golpe crítico!")

        print(f"Daño real: {resultado2['dano_real']}")
        print(f"Vida restante de {resultado2['defensor']}: {resultado2['vida_restante']}")

        if not resultado2["defensor_sigue_vivo"]:
            print(f"{personaje1['nombre']} ha sido derrotado")
            break

        turno += 1


#Funcion para unir estadisticas de equipo a las del personaje, sumando las bonificaciones de los items equipados a las estadísticas base del personaje.

def calcular_bonus_equipo(items_equipados):
    bonus_total = {
        "fuerza": 0,
        "defensa": 0,
        "velocidad": 0,
        "critico": 0,
        "vida_max": 0,
        "mana": 0
    }

    for item in items_equipados:
        if "bonus" in item:
            for stat in item["bonus"]:
                if stat in bonus_total:
                    bonus_total[stat] += item["bonus"][stat]

    return bonus_total

def obtener_stats_combate(personaje, items_equipados=None):
    stats_finales = {
        "vida_max": personaje["vida_max"],
        "mana": personaje["mana"],
        "fuerza": personaje["estadisticas"]["fuerza"],
        "defensa": personaje["estadisticas"]["defensa"],
        "velocidad": personaje["estadisticas"]["velocidad"],
        "critico": personaje["estadisticas"]["critico"]
    }

    if items_equipados is not None:
        bonus = calcular_bonus_equipo(items_equipados)

        for stat in bonus:
            if stat in stats_finales:
                stats_finales[stat] += bonus[stat]

    return stats_finales

personaje1 = crear_personaje("Ragnar", "Guerrero")
personaje2 = crear_personaje("Mirella", "Arquera")

espada = {
    "id_item": 101,
    "nombre": "Espada de hierro",
    "tipo": "equipable",
    "cantidad": 1,
    "equipado": True,
    "bonus": {
        "fuerza": 5
    }
}

escudo = {
    "id_item": 102,
    "nombre": "Escudo de roble",
    "tipo": "equipable",
    "cantidad": 1,
    "equipado": True,
    "bonus": {
        "defensa": 4
    }
}

arco_largo = {
    "id_item": 103,
    "nombre": "Arco largo",
    "tipo": "equipable",
    "cantidad": 1,
    "equipado": True,
    "bonus": {
        "fuerza": 3,
        "critico": 10
    }
}

equipo_ragnar = [espada, escudo]
equipo_mirella = [arco_largo]

resultado = atacar(personaje1, personaje2, equipo_ragnar, equipo_mirella)

print(resultado)
print(personaje1)
print(personaje2)

personaje1 = crear_personaje("Ragnar", "Guerrero")
personaje2 = crear_personaje("Mirella", "Arquera")

combate_simple(personaje1, personaje2)