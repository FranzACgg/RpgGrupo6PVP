from enemigos_dialogos import dialogo_de_enemigo, obtener_dialogo, ENCUENTRO, DERROTA
from dialogos_comercio import (
    precio_de_venta,
    sumar_oro,
    restar_oro,
    cantidad_de_oro,
)


def test_obtener_dialogo_devuelve_frase_conocida():
    assert dialogo_de_enemigo({"tipo": "slime"}, ENCUENTRO) == "Glup...? Glup glup!"
    assert obtener_dialogo("GOBLIN", DERROTA) == "No... esta cueva era mia..."


def test_obtener_dialogo_tipo_desconocido_devuelve_vacio():
    assert obtener_dialogo("dragon", ENCUENTRO) == ""


def test_oro_se_suma_y_resta_en_el_inventario():
    inventario = []
    assert cantidad_de_oro(inventario) == 0
    sumar_oro(inventario, 50)
    assert cantidad_de_oro(inventario) == 50
    sumar_oro(inventario, 25)
    assert cantidad_de_oro(inventario) == 75
    restar_oro(inventario, 30)
    assert cantidad_de_oro(inventario) == 45


def test_precio_de_venta_mitad_o_default():
    articulos = [{"item": {"id_item": 2}, "precio": 40}]
    assert precio_de_venta(2, articulos) == 20
    assert precio_de_venta(999, articulos) == 5
