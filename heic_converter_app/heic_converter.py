from argparse import ArgumentParser
from gooey import Gooey, GooeyParser
from pathlib import Path
from PIL import Image
import pillow_heif


def convert_image(read_path, write_path):
    heif_file = pillow_heif.read_heif(read_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )

    image.save(write_path, format="jpeg")


def params_processor(read_path, write_path):
    read_path = Path(read_path)
    write_path = Path(write_path)

    if read_path.is_dir():
        assert write_path.is_dir()
        pairs = []
        for file in read_path.glob("*.heic"):
            tgt = write_path / (file.stem + ".jpeg")
            pairs.append((file, tgt))
        return pairs

    return [(read_path, write_path)]


@Gooey(program_name="HEIC Converted",
       default_size=(500, 550),
       clear_before_run=True)
def main():
    parser = GooeyParser()
    parser.add_argument("source", help="Path to Dir or File",
                        metavar="Цільова Директорія", widget="DirChooser")

    # todo not used, just for example
    group = parser.add_argument_group("Додаткові Опції")
    group.add_argument("--override", action="store_true", help="Перезаписати існуючий файл")
    group.add_argument("--delete", action="store_true", help="Видалити оригінальний файл")
    group.add_argument("--quality", default=1, widget="DecimalField",
                       action="store", help="Якість")
    group.add_argument("--format", default="jpeg", choices=["jpeg", "png"],
                       widget="Dropdown", help="Формат вихідного зображення")

    args = parser.parse_args()

    print(f"Вказана директорія: {args.source}")
    path_pairs = params_processor(args.source, args.source)
    print(f"Знайдено: {len(path_pairs)}")

    for pair in path_pairs:
        convert_image(*pair)
    print("Обробка виконана успішно")


main()
