from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message

from resolvers import Resolvers

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: Message, resolvers: Resolvers):
    await resolvers.start(message)


@router.message(Command("calc"))
async def handle_calc(
    message: Message,
    command: CommandObject,
    resolvers: Resolvers,
):
    # CommandObject - полегшує парсинг аргументів команди
    await resolvers.calc(message, command)


@router.message(Command("config"))
async def handle_config(
    message: Message,
    command: CommandObject,
    resolvers: Resolvers,
):
    await resolvers.config(message, command)
