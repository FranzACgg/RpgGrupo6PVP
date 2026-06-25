from pantalla_batalla import _danio_recibido


def test_danio_recibido_resta_defensa():
    assert _danio_recibido(40, 30) == 10


def test_danio_recibido_piso_25_por_ciento():
    # con mucha defensa, igual pasa el 25% del ataque
    assert _danio_recibido(40, 100) == 10
    assert _danio_recibido(35, 70) == 9


def test_danio_recibido_sin_defensa_pasa_todo():
    assert _danio_recibido(40, 0) == 40
