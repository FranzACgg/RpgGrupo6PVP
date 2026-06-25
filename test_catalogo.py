from catalogo import cargar_catalogo, item_aleatorio


def test_item_aleatorio_devuelve_un_item_con_keys_de_item():
    cargar_catalogo()
    item = item_aleatorio()
    for key in ("id_item", "nombre", "tipo", "cantidad", "equipado"):
        assert key in item


def test_item_aleatorio_devuelve_copia_no_referencia():
    cargar_catalogo()
    item = item_aleatorio()
    item["cantidad"] = 999
    otro = item_aleatorio()
    # mutar la copia devuelta no afecta a futuras lecturas del catalogo
    assert otro["cantidad"] != 999 or otro["id_item"] != item["id_item"]
