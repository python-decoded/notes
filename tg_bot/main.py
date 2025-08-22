from pydantic import BaseModel


class Config(BaseModel):
    height: float
    width: float
    length: float
    weight: float

    @property
    def volume(self):
        return self.height * self.width * self.length


def calculate(height, width, length, config: Config):
    volume = height * width * length
    return round(volume / config.volume * config.weight, 2)

# =============================================================================

class ConfigManager:
    DEFAULT = Config(height=42, width=70, length=40, weight=30)

    def __init__(self):
        self.data = {}

    async def get(self, key) -> Config:
        attrs = self.data.get(key)
        return attrs and Config(**attrs) or self.DEFAULT

    async def set(self, key, config: Config):
        self.data[key] = config.model_dump()

# ============================================================================


import os
import re
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


class Resolvers:

    def __init__(self):
        self.config_manager = ConfigManager()

    async def start(self, msg: Message):
        # Приклад повідомлення:  '/start'

        config = await self.config_manager.get(msg.chat.id)

        await msg.answer(
            "Вітаю!\n"
            f"Еталонна коробка: {config.width}х{config.height}х{config.length} = {config.weight} кг.\n"
            "Розрахувати вагу коробки: '/calc L W H'\n"
            "Змінити конфігурацію: '/config L W H WIDTH'")


    async def calc(self, msg: Message):
        # Приклад повідомлення:  '/calc  34.5 21  15'

        try:
            text = msg.text.removeprefix("/calc")
            l, w, h = [float(i) for i in re.split(" +", text) if i]
            config = await self.config_manager.get(msg.chat.id)
            res = calculate(l, w, h, config)
            await msg.answer(f"{l}x{w}x{h} = {res} кг.")
        except:
            await msg.answer(f"Невірно виконана команда. Спробуй ще раз")


    async def config(self, msg: Message):
        # Приклад повідомлення:  '/config  34.5 21  15 20'

        try:
            text = msg.text.removeprefix("/config")
            l, w, h, weight = [float(i) for i in re.split(" +", text) if i]
            config = Config(height=h, width=w, length=l, weight=weight)
            await self.config_manager.set(msg.chat.id, config)
            await msg.answer(f"Нова конфігурація: {l}x{w}x{h} = {weight} кг.")
        except:
            await msg.answer(f"Невірно виконана команда. Спробуй ще раз")


if __name__ == "__main__":

    # створюємо бота
    resolvers = Resolvers()
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    dp = Dispatcher()

    # реєструємо обробники
    dp.message.register(resolvers.start, Command("start"))
    dp.message.register(resolvers.calc, F.text.startswith("/calc"))
    dp.message.register(resolvers.config, F.text.startswith("/config"))

    # запускаємо обробку вхідних повідомлень
    asyncio.run(dp.start_polling(bot))
