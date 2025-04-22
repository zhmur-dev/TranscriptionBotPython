from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.messages.start_msg import MESSAGES

start_router = Router()


@start_router.message(CommandStart())
async def transcribe_audio(message: Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer(text=MESSAGES.get('hello'))
