import re
from collections import deque


def tiene_cerrado_los_signos(
    valor: str, símbolo_apertura: str, símbolo_cierre: str
) -> bool:
    stack = deque()
    for char in valor:
        if char == símbolo_apertura:
            stack.append(char)
        elif char == símbolo_cierre and len(stack) == 0:
            return False
        elif char == símbolo_cierre:
            stack.pop()
    return len(stack) == 0


def mayúsculas_son_correctas(valor: str) -> bool:
    acerción = re.search(r"(?<=[^\.1-9])\.\s[a-z]", valor)
    return acerción is None


def minúsculas_son_correctas(valor: str) -> bool:
    if valor.isupper():
        return True
    valor = _filtrar_nombres(valor)
    acerción = re.search(r"(?<=\w)\,\s[A-Z]", valor)
    return acerción is None

def _filtrar_nombres(valor) -> str:
    nombres = ["Kris", "Susie", "Ralsei", "Tenna", "Láncer", "Ruddin", "Hatti", "Noelle", "Ásriel", "Roulxs", "K_K", "Jockington", "PAPYRUS",
    "ALPHYS",
    "UNDYNE",
    "RUDY",
    "BERDLY",
    "CATTY",
    "CATTI",
    "BRATTY",
    "GERSON",
    "JOCKINGTON",]
    for nombre in nombres:
        valor = valor.replace(nombre.lower().capitalize(), nombre.lower())
    return valor
