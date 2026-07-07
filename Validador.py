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
    acerción = re.search(r"(?<=\w)\,\s[A-Z]", valor)
    return acerción is None
