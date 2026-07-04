# Scripts-Para-Traducci-n-Deltarune

## Requisitos

- Python 3.10 o superior
- Dependencias:

```bash
pip install -r "requirements.txt"
```

# Verificador de signos en archivos JSON

Una utilidad de línea de comandos escrita en Python que analiza los valores de un archivo JSON y detecta signos de puntuación sin cerrar.

Actualmente verifica:

- Signos de interrogación (`¿ ?`)
- Signos de exclamación (`¡ !`)
- Paréntesis (`( )`)

Es especialmente útil para revisar archivos de traducción o localización antes de publicarlos.

## Características

- Muestra una tabla con las entradas problemáticas.
- Permite imprimir únicamente las claves que contienen errores.

## Uso

```bash
python main.py archivo.json
```

Salida de ejemplo:

```
    Faltan cerrar signos de pregunta en:

clave                     texto
menu.start                ¿Comenzar
dialog.hello              ¿Cómo estás
```

## Mostrar solo las claves con errores

```bash
python main.py archivo.json --solo_claves
```

o

```bash
python main.py archivo.json -c
```

## Formato esperado

El programa espera un JSON con pares clave-valor donde los valores sean cadenas de texto.

Ejemplo:

```json
{
    "menu.play": "Jugar",
    "dialog.greeting": "¿Cómo estás?",
    "dialog.error": "¿Qué sucede"
}
```

En este ejemplo se reportará `dialog.error`.

No valida:

- Comillas.
- Corchetes o llaves.
- Anidamientos incorrectos entre distintos tipos de signos.
- Reglas ortográficas de la RAE; únicamente verifica que los signos estén balanceados.
