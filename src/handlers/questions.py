import logging
import os

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from src.messages.questions_msg import MESSAGES
from src.utils.states import FSMTranscriptionStage

questions_router = Router()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'  # noqa
)


@questions_router.message(Command(commands='questions'))
async def extract_questions(message: Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer(text=MESSAGES.get('select_file'))
    await state.set_state(FSMTranscriptionStage.managing_questions)


@questions_router.message(
    F.document,
    StateFilter(FSMTranscriptionStage.managing_questions)
)
async def handle_text_file(message: Message, bot: Bot, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    file_path = file.file_path
    downloaded_file = await bot.download_file(file_path)

    content = downloaded_file.read().decode('utf-8')
    filtered_lines = [line for line in content.splitlines() if line.strip().endswith('?')]

    await message.answer(text='\n'.join(filtered_lines))
    await state.set_state(state=None)
