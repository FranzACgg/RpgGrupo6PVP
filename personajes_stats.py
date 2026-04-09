
# funcion def para crear personajes con nombres de mitologia nordica juego rpg usando diccionarios
def crear_personaje(nombre, clase, nivel):
    personaje = {
        "nombre": nombre,
        "clase": clase,
        "nivel": nivel
    }
    return personaje
personaje1 = crear_personaje("Thor", "Guerrero", 10)
print(personaje1)
personaje2 = crear_personaje("Loki", "Mago", 8)
print(personaje2)
personaje3 = crear_personaje("Freya", "Arquera", 12)
print(personaje3)
personaje4 = crear_personaje("Odin", "Sacerdote", 15)
print(personaje4)

# funcion def para asignar estadisticas a los personajes creados con la funcion anterior, utilizando diccionarios anidados
def asignar_estadisticas(personaje, fuerza, destreza, inteligencia):
    personaje["estadisticas"] = {
        "fuerza": fuerza,
        "destreza": destreza,
        "inteligencia": inteligencia
    }
    return personaje
personaje1 = asignar_estadisticas(personaje1, 10, 5, 3)
print(personaje1)
personaje2 = asignar_estadisticas(personaje2, 3, 7, 10)
print(personaje2)
personaje3 = asignar_estadisticas(personaje3, 5, 10, 5)
print(personaje3)
personaje4 = asignar_estadisticas(personaje4, 7, 3, 10)
print(personaje4)   