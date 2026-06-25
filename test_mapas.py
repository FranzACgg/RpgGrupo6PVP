from mapa_prado import generar_mapa_prado
from mapa_mercado import generar_mapa_mercado_total
from mapa_cementerio import generar_mapa_cementerio
from mapa_coliseo import generar_mapa_coliseo
from mapa_cueva import generar_mapa_cueva


def _es_grilla(mapa):
    return (
        type(mapa) == list and len(mapa) > 0 and type(mapa[0]) == list
    )


def test_generadores_de_mapa_devuelven_grilla():
    assert _es_grilla(generar_mapa_prado())
    assert _es_grilla(generar_mapa_mercado_total())
    assert _es_grilla(generar_mapa_cementerio())
    assert _es_grilla(generar_mapa_coliseo())
    assert _es_grilla(generar_mapa_cueva())


def test_prado_no_tiene_jugador_dibujado():
    # el jugador se dibuja al entrar/moverse, no debe quedar una 'P' fija en el mapa
    mapa = generar_mapa_prado()
    for fila in mapa:
        assert "P" not in fila
