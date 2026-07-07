import argparse
import json

import tabulate

from Validador import (
    mayúsculas_son_correctas,
    minúsculas_son_correctas,
    tiene_cerrado_los_signos,
)


def print_in_table(advertencias, message):
    table = {
        "texto": advertencias.values(),
        "clave": advertencias.keys(),
    }
    headers = ["clave", "texto"]
    print("\n\t----" + message + "----")
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
    advertencias_mayúsculas_erroneas = {}
    advertencias_minúsculas_erroneas = {}
    for clave in data:
        if not tiene_cerrado_los_signos(data[clave], "¿", "?"):
            advertencias_signos_pregunta[clave] = rf"{data[clave]}"
        if not tiene_cerrado_los_signos(data[clave], "(", ")"):
            advertencias_signos_paréntesis[clave] = rf"{data[clave]}"
        if not tiene_cerrado_los_signos(data[clave], "¡", "!"):
            advertencias_signos_exclamación[clave] = rf"{data[clave]}"
        if not mayúsculas_son_correctas(data[clave]):
            advertencias_mayúsculas_erroneas[clave] = rf"{data[clave]}"
        if not minúsculas_son_correctas(data[clave]):
            advertencias_minúsculas_erroneas[clave] = rf"{data[clave]}"
    advertencias_unificadas = {
        **advertencias_signos_exclamación,
        **advertencias_signos_pregunta,
        **advertencias_signos_paréntesis,
        **advertencias_mayúsculas_erroneas,
        **advertencias_minúsculas_erroneas,
    }
    if args.solo_claves:
        for clave in advertencias_unificadas:
            print(clave)
    else:
        frase_signos = "Faltan abrir o cerrar signos de "
        print_in_table(advertencias_signos_pregunta, frase_signos + "pregunta en")
        print_in_table(advertencias_signos_exclamación, frase_signos + "exclamación en")
        print_in_table(advertencias_signos_paréntesis, frase_signos + "paréntesis en")
        print_in_table(
            advertencias_mayúsculas_erroneas, "minúsculas después de punto en"
        )
        print_in_table(
            advertencias_minúsculas_erroneas, "mayusculas después de comas en"
        )
    if not (
        advertencias_signos_exclamación
        or advertencias_signos_paréntesis
        or advertencias_signos_pregunta
    ):
        print("Todo en orden :)")


if __name__ == "__main__":
    main()
