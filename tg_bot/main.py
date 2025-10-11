import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from domain import Calculator, ConfigManager
from handlers import router
from resolvers import Resolvers


async def startup(bot: Bot) -> None:
    # Відкидаємо апдейти які накопичились за час що бот не працював
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot started.")


async def main():
    # Використовуємо .env file якщо він існує
    load_dotenv()

    # Контекст менеджер закриває сесію бота
    async with Bot(token=os.environ["TELEGRAM_TOKEN"]) as bot:
        dp = Dispatcher()

        # Dependency injection
        calculator = Calculator()
        config_manager = ConfigManager()
        resolvers = Resolvers(config_manager, calculator)

        # https://docs.aiogram.dev/en/latest/dispatcher/dependency_injection.html
        dp["resolvers"] = resolvers

        # Включаємо роутери з різних - це розвантажує код основного модуля
        dp.include_router(router)
        dp.startup.register(startup)

        # запускаємо обробку вхідних повідомлень
        await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Мабуть ми не хочемо бачити стек трейс при Ctrl+C
        print("Stopped by user.")
