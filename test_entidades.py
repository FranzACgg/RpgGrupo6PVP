from config import crear_contexto
from entidades import (
    generar_enemigos_prado,
    generar_enemigos_cueva,
    buscar_enemigo_en,
    eliminar_enemigo,
)


def test_generar_enemigos_prado_devuelve_slimes_con_hp():
    enemigos = generar_enemigos_prado()
    assert len(enemigos) > 0
    for en in enemigos:
        assert en["tipo"] == "slime"
        assert en["hp_actual"] > 0


def test_generar_enemigos_cueva_devuelve_goblins():
    enemigos = generar_enemigos_cueva()
    assert len(enemigos) > 0
    for en in enemigos:
        assert en["tipo"] == "goblin"


def test_buscar_enemigo_en_encuentra_por_posicion():
    contexto = crear_contexto()
    contexto["mundo"]["enemigos"] = [
        {"tipo": "slime", "pos": [5, 5], "debajo": ",", "hp_actual": 50}
    ]
    assert buscar_enemigo_en([5, 5], contexto) is not None
    assert buscar_enemigo_en([0, 0], contexto) is None


def test_eliminar_enemigo_lo_saca_de_la_lista_y_da_drop():
    contexto = crear_contexto()
    contexto["inventario"] = []
    enemigo = {"tipo": "slime", "pos": [2, 2], "debajo": ".", "hp_actual": 50}
    contexto["mundo"]["enemigos"] = [enemigo]
    mapa = [[" "] * 10 for _ in range(10)]

    eliminar_enemigo(enemigo, mapa, contexto)

    assert enemigo not in contexto["mundo"]["enemigos"]
    assert len(contexto["inventario"]) == 1  # baba de slime
