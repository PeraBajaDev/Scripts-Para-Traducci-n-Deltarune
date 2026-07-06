import argparse
from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Args:
    file_path: str
    to_find: str
    as_replace: str
    # is_case_sensitive: bool


def main():
    parser: ArgumentParser = argparse.ArgumentParser()
    _ = parser.add_argument("file_path", help="ruta del archivo txt.", type=str)
    _ = parser.add_argument(
        "to_find",
        help="la palabra o frase a reemplazar (es sensible a mayúsculas).",
        type=str,
    )
    _ = parser.add_argument(
        "as_replace",
        help="la palabra o frase con la cual se reemplaza.",
        type=str,
    )
    # _ = parser.add_argument(
    #    "--case_sensitive", const="store_true", nargs="?", required=False
    # )
    new_lines: list[list[str]] = []
    namespace = parser.parse_args()
    args: Args = Args(
        namespace.file_path,
        namespace.to_find,
        namespace.as_replace,
        # namespace.case_sensitive,
    )
    with open(args.file_path, "r", encoding="utf-8") as txt:
        for line in txt.readlines():
            values: list[str] = line.split(";")
            if not values[1].startswith("Content:"):
                new_lines.append(values)
                continue
            content = values[1].removeprefix("Content:")
            if args.to_find in content:
                content = content.replace(args.to_find, args.as_replace)
                print("old_line:", values[1], "| new line:", content)
            values[1] = "Content:" + content
            new_lines.append(values)

    with open(args.file_path, "w", encoding="utf-8") as txt:
        text = "".join([";".join(l) for l in new_lines])
        _ = txt.write(text)


if __name__ == "__main__":
    main()
