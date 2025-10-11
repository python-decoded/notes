from aiogram.filters import CommandObject
from aiogram.types import Message

from domain import Calculator, Config, ConfigManager

# Взагалі коду тут небагато можна було і без класу Resolvers обійтись
# - пистати це все у хендлерах, крім того назва у цього класа не дуже.

# Але якщо розвивати тему абстрактного коня у вакуммі:
# Calculator & ConfigManager - можуть стати інтерфейсами/абстрактними класами
# якщо раптом треба буде гнучко змінювати поведінку.

# Це все добре, але на практиці трохи оверінджинірінг

DEFAULT_CONFIG = Config(height=42, width=70, length=40, weight=30)


class Resolvers:
    def __init__(self, config_manager: ConfigManager, calculator: Calculator):
        self.config_manager = config_manager
        self.calculator = calculator

    async def start(self, msg: Message) -> None:
        # Приклад повідомлення:  '/start'
        config = (await self.config_manager.get(msg.chat.id)) or DEFAULT_CONFIG
        await msg.answer(
            "Вітаю!\n"
            f"Еталонна коробка: {config.width}х{config.height}х"
            f"{config.length} = {config.weight} кг.\n"
            "Розрахувати вагу коробки: '/calc L W H'\n"
            "Змінити конфігурацію: '/config L W H WIDTH'"
        )

    async def calc(self, msg: Message, command: CommandObject) -> None:
        # Приклад повідомлення:  '/calc  34.5 21  15'
        success = False
        if args := command.args and command.args.split(maxsplit=2):
            try:
                length, width, height = list(map(float, args))
                config = (
                    await self.config_manager.get(msg.chat.id)
                    or DEFAULT_CONFIG
                )
                result = self.calculator.calculate(
                    length,
                    width,
                    height,
                    config,
                )
                await msg.answer(
                    f"{length}x{width}x{height} = {result:.2f} кг."
                )
                success = True
            except ValueError:
                pass

        if not success:
            await msg.answer("Невірно виконана команда. Спробуй ще раз")

    async def config(self, msg: Message, command: CommandObject) -> None:
        # Приклад повідомлення:  '/config  34.5 21  15 20'
        success = False
        if args := command.args and command.args.split(maxsplit=3):
            try:
                length, width, height, weight = list(map(float, args))
                config = Config(
                    height=height,
                    width=width,
                    length=length,
                    weight=weight,
                )
                await self.config_manager.set(msg.chat.id, config)
                await msg.answer(
                    f"Нова конфігурація: "
                    f"{length}x{width}x{height} = {weight} кг."
                )
                success = True
            except ValueError:
                pass

        if not success:
            await msg.answer("Невірно виконана команда. Спробуй ще раз")
