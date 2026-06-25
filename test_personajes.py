from personajes import (
    crear_personaje,
    recibir_danio,
    curar,
    esta_vivo,
    usar_habilidad,
    revivir,
    obtener_stats_con_equipamiento,
)


def test_crear_personaje_valido_arranca_con_3_vidas():
    p = crear_personaje("Ragnar", "Guerrero")
    assert p["nombre"] == "Ragnar"
    assert p["vidas"] == 3
    assert p["stats_actuales"]["hp"] == p["stats_base"]["hp"]


def test_crear_personaje_clase_invalida_devuelve_none():
    assert crear_personaje("Nadie", "ClaseQueNoExiste") is None


def test_recibir_danio_fisico_resta_defensa_y_minimo_uno():
    p = crear_personaje("Ragnar", "Guerrero")  # defensa 45
    hp_inicial = p["stats_actuales"]["hp"]
    danio = recibir_danio(p, 50, "fisico")     # 50 - 45 = 5
    assert danio == 5
    assert p["stats_actuales"]["hp"] == hp_inicial - 5
    # daño que no supera la defensa igual hace 1
    assert recibir_danio(p, 1, "fisico") == 1


def test_recibir_danio_no_baja_de_cero():
    p = crear_personaje("Morgan", "Pirata")
    recibir_danio(p, 99999, "otro")
    assert p["stats_actuales"]["hp"] == 0
    assert esta_vivo(p) is False


def test_curar_no_supera_el_maximo():
    p = crear_personaje("Ragnar", "Guerrero")
    recibir_danio(p, 100, "otro")
    curado = curar(p, 99999)
    assert p["stats_actuales"]["hp"] == p["stats_base"]["hp"]
    assert curado <= p["stats_base"]["hp"]


def test_usar_habilidad_sin_mp_devuelve_none():
    p = crear_personaje("Ragnar", "Guerrero")
    p["stats_actuales"]["mp"] = 0
    assert usar_habilidad(p, 0) is None


def test_usar_habilidad_indice_invalido_devuelve_none():
    p = crear_personaje("Ragnar", "Guerrero")
    assert usar_habilidad(p, 99) is None


def test_revivir_gasta_una_vida_y_restaura_stats():
    p = crear_personaje("Ragnar", "Guerrero")
    recibir_danio(p, 99999, "otro")
    assert revivir(p) is True
    assert p["vidas"] == 2
    assert p["stats_actuales"]["hp"] == p["stats_base"]["hp"]


def test_revivir_sin_vidas_devuelve_false():
    p = crear_personaje("Ragnar", "Guerrero")
    p["vidas"] = 0
    assert revivir(p) is False


def test_obtener_stats_con_equipamiento_suma_efectos():
    p = crear_personaje("Ragnar", "Guerrero")
    base_fuerza = p["stats_base"]["fuerza"]
    items = [{"efecto": {"fuerza": 10}}]
    stats = obtener_stats_con_equipamiento(p, items)
    assert stats["fuerza"] == base_fuerza + 10


def test_recibir_danio_magico_no_crashea():
    p = crear_personaje("Loki", "Bufon")
    danio = recibir_danio(p, 50, "magico")
    assert danio >= 1
