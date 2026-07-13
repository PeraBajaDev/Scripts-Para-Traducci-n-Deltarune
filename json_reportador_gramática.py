import argparse
from dataclasses import dataclass, field
import json
from prompt_toolkit import prompt
import tabulate
import subprocess
import os
from Validador import (
    mayúsculas_son_correctas,
    minúsculas_son_correctas,
    tiene_cerrado_los_signos,
)

@dataclass
class Advertencias:
    @staticmethod
    def _factory():
        return {}
    signos_pregunta: dict[str, str] = field(default_factory=_factory)  # noqa: F821
    signos_exclamación: dict[str, str] = field(default_factory=_factory)
    signos_paréntesis: dict[str, str] = field(default_factory=_factory)
    mayúsculas_erroneas: dict[str, str] = field(default_factory=_factory)
    minúsculas_erroneas: dict[str, str] = field(default_factory=_factory)

    def obtener_unificadas(self) -> dict[str, str]:
        advertencias_unificadas = {
            **self.signos_exclamación,
            **self.signos_pregunta,
            **self.signos_paréntesis,
            **self.mayúsculas_erroneas,
            **self.minúsculas_erroneas,
        }
        return advertencias_unificadas


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
def entrar_modo_interactivo(advertencias: Advertencias,
data: dict, ruta_archivo_json: str):
    data = data.copy()
    advertencias_unificadas = advertencias.obtener_unificadas()
    for clave in advertencias_unificadas:
        subprocess.run("cls" if os.name == "nt" else "clear")
        print(clave + ":", advertencias_unificadas[clave])
        corrección = prompt("su corrección:", default=advertencias_unificadas[clave])
        data[clave] = corrección
    with open(ruta_archivo_json, "w", encoding="utf-8") as archivo_json:
         json.dump(data, archivo_json, indent=4, ensure_ascii=False)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ruta_archivo_json")
    parser.add_argument(
        "-solo_claves",
        "-c",
        help="Solo muestra las claves que tienen el error",
        action="store_true",
    )
    parser.add_argument(
        "-interactivo",
        "-i",
        help="Va mostrando cada error y permite ir corrigiendo sobre la marcha",
        action="store_true",
    )
    data: dict = {}
    args = parser.parse_args()
    with open(args.ruta_archivo_json, "r") as archivo_json:
        data = json.load(archivo_json)
    advertencias = Advertencias()
    for clave in data:
        if not tiene_cerrado_los_signos(data[clave], "¿", "?"):
            advertencias.signos_pregunta[clave] = rf"{data[clave]}"
        if not tiene_cerrado_los_signos(data[clave], "(", ")"):
            advertencias.signos_paréntesis[clave] = rf"{data[clave]}"
        if not tiene_cerrado_los_signos(data[clave], "¡", "!"):
            advertencias.signos_exclamación[clave] = rf"{data[clave]}"
        if not mayúsculas_son_correctas(data[clave]):
            advertencias.mayúsculas_erroneas[clave] = rf"{data[clave]}"
        if not minúsculas_son_correctas(data[clave]):
            advertencias.minúsculas_erroneas[clave] = rf"{data[clave]}"

    if args.interactivo:
        entrar_modo_interactivo(advertencias, data, args.ruta_archivo_json)
    if args.solo_claves:
        for clave in advertencias.obtener_unificadas():
            print(clave)
    else:
        frase_signos = "Faltan abrir o cerrar signos de "
        print_in_table(advertencias.signos_pregunta, frase_signos + "pregunta en")
        print_in_table(advertencias.signos_exclamación, frase_signos + "exclamación en")
        print_in_table(advertencias.signos_paréntesis, frase_signos + "paréntesis en")
        # print_in_table(
        #     advertencias_mayúsculas_erroneas, "minúsculas después de punto en"
        # )
        # print_in_table(
        #     advertencias_minúsculas_erroneas, "mayusculas después de comas en"
        # )
    if not (
        advertencias.signos_exclamación
        or advertencias.signos_paréntesis
        or advertencias.signos_pregunta
    ):
        print("Todo en orden :)")


if __name__ == "__main__":
    main()
