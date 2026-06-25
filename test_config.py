from config import crear_contexto, aplicar_efecto_consumible
from personajes import crear_personaje


def test_crear_contexto_tiene_estructura_esperada():
    contexto = crear_contexto()
    assert contexto["estado_actual"] is None
    assert type(contexto["progreso"]["enemigos_derrotados"]) == set
    assert contexto["progreso"]["coliseo_completado"] is False
    assert "mundo" in contexto


def test_aplicar_efecto_consumible_cura_hp():
    personaje = crear_personaje("Ragnar", "Guerrero")
    personaje["stats_actuales"]["hp"] = 10
    aplicar_efecto_consumible({"id_item": 1}, personaje)  # id 1 = +50 hp
    assert personaje["stats_actuales"]["hp"] == 60


def test_aplicar_efecto_consumible_super_curacion_sube_maximo():
    personaje = crear_personaje("Ragnar", "Guerrero")
    hp_max_inicial = personaje["stats_base"]["hp"]
    aplicar_efecto_consumible({"id_item": 60}, personaje)  # super_curacion
    assert personaje["stats_base"]["hp"] == hp_max_inicial + 50
    assert personaje["stats_actuales"]["hp"] == personaje["stats_base"]["hp"]
