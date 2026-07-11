# voice recognition
# pip install torch openai-whisper

import os
from functools import lru_cache
import whisper
from gooey import Gooey, GooeyParser


def resolve_device(device_choice: str) -> str:
    import torch

    if device_choice == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"

    if device_choice == "cuda" and not torch.cuda.is_available():
        print("CUDA selected, but no compatible GPU was found. Falling back to CPU.")
        return "cpu"

    if device_choice == "cuda":
        print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Using CPU.")

    return device_choice


@lru_cache
def get_model(*, model: str = "base", device: str = "auto"):
    print(f"Завантаження моделі Whisper ({model})... Будь ласка, зачекайте.")

    try:
        device = resolve_device(device)
    except Exception as e:
        print("torch не зміг визначити device для моделі розпізнавання голосу.\n "
              "Буде використаний по замовчуванню.\n "
              f"{e}")
        device = None

    model = whisper.load_model(model, device=device)
    return model


def transcribe_audio(audio_file: str, output: str = None,
                     language: str = "uk", timestamps: bool = False,
                     device: str = "auto", model: str = "custom"):

    model = model if model in ["tiny", "base", "small", "medium", "large", "turbo"] else "base"
    device = device if device in ["auto", "cuda", "cpu"] else "auto"
    language = language if language in [None, "uk", "en", "pl", "de", "es", "fr", "it"] else None

    # Перевірка наявності файлу
    if not os.path.exists(audio_file):
        print(f"Помилка: Файл '{audio_file}' не знайдено.")
        return

    if not output:
        output = audio_file.rsplit(".", 1)[0] + "__transcript.txt"

    model = get_model(model=model, device=device)
    use_fp16 = model.device == "cuda"

    transcribe_args = {}
    if language:
        transcribe_args['language'] = language
        print(f"Примусово встановлено мову: {language}")
    else:
        print("Мова визначиться автоматично під час аналізу...")

    print(f"\nАналіз файлу '{os.path.basename(audio_file)}' розпочато.")
    print("Це може зайняти деякий час залежно від довжини аудіо та моделі...\n")

    result = model.transcribe(audio_file, fp16=use_fp16, **transcribe_args)

    # Запис у файл
    with open(output, "w", encoding="utf-8") as f:
        if timestamps:
            print("Форматування тексту з таймкодами...")
            for segment in result["segments"]:
                start = format_time(segment["start"])
                end = format_time(segment["end"])
                text = segment["text"].strip()
                f.write(f"[{start} -> {end}] {text}\n")
        else:
            print("Форматування чистого тексту...")
            f.write(result["text"].strip())

    print(f"\n🎉 Процес завершено успішно!")
    print(f"Текст збережено у: {output}\n")


def format_time(seconds: float) -> str:
    """Перетворює секунди у зручний формат часу HH:MM:SS"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"


def main():
    # Замість звичайного ArgumentParser використовуємо GooeyParser
    parser = GooeyParser(
        description="Графічний інтерфейс для розпізнавання аудіо за допомогою OpenAI Whisper."
    )

    # Створюємо групи для гарного розділення параметрів у вікні
    file_group = parser.add_argument_group("Файли")
    settings_group = parser.add_argument_group("Налаштування Whisper")

    # Обов'язковий файл (перетворюється на вікно вибору файлу)
    file_group.add_argument(
        "input",
        type=str,
        widget="FileChooser",
        help="Оберіть аудіофайл для розпізнавання (MP3, WAV тощо)"
    )

    # Вихідний файл (перетворюється на вікно збереження файлу)
    file_group.add_argument(
        "-o", "--output",
        type=str,
        widget="FileSaver",
        default="result.txt",
        help="Куди зберегти текстовий результат"
    )

    # Налаштування таймкодів (перетворюється на чекбокс / галочку)
    settings_group.add_argument(
        "-t", "--timestamps",
        action="store_true",
        help="Додати таймкоди до тексту (наприклад: [00:01:23 -> 00:01:28])"
    )

    # Опційний параметр мови (перетворюється на випадаючий список найпопулярніших мов)
    settings_group.add_argument(
        "-l", "--language",
        type=str,
        default=None,
        widget="Dropdown",
        choices=[None, "uk", "en", "pl", "de", "es", "fr", "it"],
        help="Оберіть мову (None — визначити автоматично)"
    )

    # Вибір моделі (перетворюється на випадаючий список)
    settings_group.add_argument(
        "-m", "--model",
        type=str,
        default="base",
        widget="Dropdown",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],  # medium - 1.42 GB
        help="Розмір моделі Whisper (чим більша — тим точніша, але повільніша)"
    )

    settings_group.add_argument(
        "-d", "--device",
        type=str,
        default="auto",
        widget="Dropdown",
        choices=["auto", "cuda", "cpu"],
        help="Device for Whisper: auto, cuda, or cpu"
    )

    args = parser.parse_args()
    transcribe_audio(audio_file=args.input, output=args.output,
                     language=args.language, timestamps=args.timestamps,
                     device=args.device, model=args.model)


if __name__ == "__main__":
    gooey = Gooey(
        program_name="Whisper Transcriber",
        default_size=(600, 720),
        progress_regex=r"^ Progress: (?P<current>\d+)/(?P<total>\d+)",  # Для майбутнього прогрес-бару
        navigation="Tabbed"
    )
    gooey(main)()
