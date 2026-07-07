import Validador


def test_texto_debería_tener_mayúsculas_después_de_punto():
    assert Validador.mayúsculas_son_correctas("Hola. Este, Hola")


def test_texto_debería_tener_minúsculas_despues_de_punto():
    assert not Validador.mayúsculas_son_correctas("Hola. este, Hola")


def test_texto_debería_tener_minúsculas_después_de_coma():
    assert Validador.minúsculas_son_correctas("Hola. Este, hola, papola")


def test_texto_debería_tener_mayúsculas_después_de_coma():
    assert not Validador.minúsculas_son_correctas("Hola. Este, hola, Papola")
