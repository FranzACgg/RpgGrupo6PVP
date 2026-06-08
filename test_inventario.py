"""
Grupo 1 — operan sobre el inventario y devuelven algo o lo modifican:
crear_inventario, agregar_item, busqueda_item_por_id, usar_item, manejar_equipado_item, exportar_items_equipados, descartar_item

    items_prueba = [
        {
            "id_item": 1,
            "nombre": "Pocion de HP pequeña",
            "tipo": "consumible",
            "cantidad": 5,
            "equipado": False,
        },

"""

from inventario import (
    crear_inventario,
    agregar_item,
    busqueda_item_por_id,
    usar_item,
)

import pytest


def test_crear_inventario():
    assert crear_inventario() == []


def test_agregar_item():
    with pytest.raises(ValueError):
        assert agregar_item(
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 5,
                "equipado": False,
                "usable": True,
            },
            [],
        )
        assert agregar_item(
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 5,
            },
            [],
        )
        assert agregar_item(
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "foo",
                "cantidad": 5,
                "equipado": False,
            },
            [],
        )
    assert (
        agregar_item(
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 5,
                "equipado": False,
            },
            [
                {
                    "id_item": 1,
                    "nombre": "Pocion de HP pequeña",
                    "tipo": "consumible",
                    "cantidad": 5,
                    "equipado": False,
                }
            ],
        )
        is True
    )
    assert (
        agregar_item(
            {
                "id_item": 31,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 5,
                "equipado": False,
            },
            [
                {
                    "id_item": i,
                    "nombre": "Pocion de HP pequeña ",
                    "tipo": "consumible",
                    "cantidad": 5,
                    "equipado": False,
                }
                for i in range(30)
            ],
        )
        is False
    )
    assert (
        agregar_item(
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 5,
                "equipado": False,
            },
            [],
        )
        is True
    )


def test_busqueda_item_por_id():
    assert (
        busqueda_item_por_id(
            1,
            [
                {
                    "id_item": 1,
                    "nombre": "Pocion de HP pequeña",
                    "tipo": "consumible",
                    "cantidad": 5,
                    "equipado": False,
                },
            ],
        )
    ) == 0
    assert (
        busqueda_item_por_id(
            1,
            [
                {
                    "id_item": 2,
                    "nombre": "Pocion de HP pequeña",
                    "tipo": "consumible",
                    "cantidad": 5,
                    "equipado": False,
                },
            ],
        )
        == -1
    )


def test_usar_item():
    assert usar_item(-1, []) is None
    assert (
        usar_item(
            0,
            [
                {
                    "id_item": 8,
                    "nombre": "Lanza Maldita",
                    "tipo": "equipable",
                    "cantidad": 1,
                    "equipado": False,
                }
            ],
        )
    ) is None
    assert (
        usar_item(
            0,
            [
                {
                    "id_item": 1,
                    "nombre": "Pocion de HP pequeña",
                    "tipo": "consumible",
                    "cantidad": 0,
                    "equipado": False,
                }
            ],
        )
    ) is None
    assert usar_item(
        1,
        [
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 1,
                "equipado": False,
            }
        ],
    ) == {
        "id_item": 1,
        "nombre": "Pocion de HP pequeña",
        "tipo": "consumible",
        "cantidad": 1,
        "equipado": False,
    }
    assert usar_item(
        1,
        [
            {
                "id_item": 1,
                "nombre": "Pocion de HP pequeña",
                "tipo": "consumible",
                "cantidad": 5,
                "equipado": False,
            }
        ],
    ) == {
        "id_item": 1,
        "nombre": "Pocion de HP pequeña",
        "tipo": "consumible",
        "cantidad": 4,
        "equipado": False,
    }
