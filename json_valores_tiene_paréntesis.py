import argparse
import json
from ast import Store
from collections import deque

import tabulate


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


# print(
#     "caso valido:",
#     caso_valido,
#     "resultado:",
#     tiene_cerrado_los_signos(caso_valido, "¿", "?"),
# )
# print(
#     "caso erroneo:",
#     caso_erroneo,
#     "resultado:",
#     tiene_cerrado_los_signos(caso_erroneo, "¿", "?"),
# )
def print_in_table(
    advertencias_signos_pregunta,
    advertencias_signos_exclamación,
    advertencias_signos_paréntesis,
):
    table = {
        "texto": advertencias_signos_pregunta.values(),
        "clave": advertencias_signos_pregunta.keys(),
    }
    headers = ["clave", "texto"]
    print("\n\tFaltan cerrar signos de pregunta en:")
    print(
        tabulate.tabulate(
            table,
            headers,
            tablefmt="plain",
            maxcolwidths=[60, 20],
        )
    )
    table = {
        "texto": advertencias_signos_exclamación.values(),
        "clave": advertencias_signos_exclamación.keys(),
    }
    print("\n\tFaltan cerrar signos de exclamación en:")
    print(
        tabulate.tabulate(
            table,
            headers,
            tablefmt="plain",
            maxcolwidths=[60, 20],
        )
    )
    table = {
        "texto": advertencias_signos_paréntesis.values(),
        "clave": advertencias_signos_paréntesis.keys(),
    }
    print("\n\tFaltan cerrar signos de paréntesis en:")
    print(
        tabulate.tabulate(
            table,
            headers,
            tablefmt="plain",
            maxcolwidths=[60, 20],
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ruta_archivo_json")
    parser.add_argument(
        "-solo_claves",
        "-c",
        help="Solo muestra las claves que tienen el error",
        action="store_true",
    )
    data: dict = {}
    args = parser.parse_args()
    with open(args.ruta_archivo_json, "r") as archivo_json:
        data = json.load(archivo_json)
    advertencias_signos_pregunta = {}
    advertencias_signos_exclamación = {}
    advertencias_signos_paréntesis = {}
    for clave in data:
        if not tiene_cerrado_los_signos(data[clave], "¿", "?"):
            advertencias_signos_pregunta[clave] = rf"{data[clave]}"
        if not tiene_cerrado_los_signos(data[clave], "(", ")"):
            advertencias_signos_paréntesis[clave] = rf"{data[clave]}"
        if not tiene_cerrado_los_signos(data[clave], "¡", "!"):
            advertencias_signos_exclamación[clave] = rf"{data[clave]}"
    if args.solo_claves:
        for clave in advertencias_signos_exclamación:
            print(clave)
        for clave in advertencias_signos_pregunta:
            print(clave)
        for clave in advertencias_signos_paréntesis:
            print(clave)
    else:
        print_in_table(
            advertencias_signos_pregunta,
            advertencias_signos_exclamación,
            advertencias_signos_paréntesis,
        )
    if not (
        advertencias_signos_exclamación
        or advertencias_signos_paréntesis
        or advertencias_signos_pregunta
    ):
        print("Todo en orden :)")


if __name__ == "__main__":
    main()
