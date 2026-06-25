from config import crear_contexto
from persistencia import (
    _serializar_contexto,
    _deserializar_contexto,
    guardar_partida,
    cargar_partida,
    existe_partida_guardada,
    borrar_partida,
    cargar_progreso,
)


def test_serializar_convierte_set_a_lista_sin_mutar_original():
    contexto = crear_contexto()
    contexto["progreso"]["enemigos_derrotados"] = {1, 2, 3}
    copia = _serializar_contexto(contexto)
    assert type(copia["progreso"]["enemigos_derrotados"]) == list
    assert sorted(copia["progreso"]["enemigos_derrotados"]) == [1, 2, 3]
    # el contexto vivo no se toca: sigue siendo un set
    assert contexto["progreso"]["enemigos_derrotados"] == {1, 2, 3}


def test_deserializar_convierte_lista_a_set():
    datos = {"progreso": {"enemigos_derrotados": [4, 5, 5]}}
    resultado = _deserializar_contexto(datos)
    assert resultado["progreso"]["enemigos_derrotados"] == {4, 5}


def test_round_trip_guardar_cargar_conserva_set_y_acentos():
    contexto = crear_contexto()
    contexto["personaje"] = {"nombre": "Ñandú con tildé"}
    contexto["progreso"]["enemigos_derrotados"] = {10, 20}
    contexto["progreso"]["coliseo_completado"] = True

    assert guardar_partida(contexto) is True
    cargado = cargar_partida()

    assert cargado["personaje"]["nombre"] == "Ñandú con tildé"
    assert cargado["progreso"]["enemigos_derrotados"] == {10, 20}
    assert cargado["progreso"]["coliseo_completado"] is True
    borrar_partida()


def test_existe_y_borrar_partida():
    contexto = crear_contexto()
    guardar_partida(contexto)
    assert existe_partida_guardada() is True
    assert borrar_partida() is True
    assert existe_partida_guardada() is False
    # borrar cuando no hay save igual devuelve True
    assert borrar_partida() is True


def test_cargar_progreso_default_cuando_no_existe():
    progreso = cargar_progreso()
    assert "clase_oculta_desbloqueada" in progreso
