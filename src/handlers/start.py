from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from src.config.config import settings
from src.services.transcription import TranscriptService
from src.messages.start_msg import MESSAGES
from src.utils.states import FSMTranscriptionStage

start_router = Router()


@start_router.message(CommandStart())
async def transcribe_audio(message: Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer(text=MESSAGES.get('select_file'))
    await state.set_state(FSMTranscriptionStage.transcription_run)


@start_router.message(
    F.video | F.audio | F.document,
    StateFilter(FSMTranscriptionStage.transcription_run)
)
async def handle_document(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(state=None)
    try:
        if message.audio:
            file_id = message.audio.file_id
            original_filename = message.audio.file_name
        elif message.video:
            file_id = message.video.file_id
            original_filename = message.video.file_name
        elif message.document:
            file_id = message.document.file_id
            original_filename = message.document.file_name
        else:
            await message.answer(text=MESSAGES.get('wrong_file_type'))
            return
        await message.answer(text=MESSAGES.get('transcription_process'))
        file = await bot.get_file(file_id)
        file_path = file.file_path
        service = TranscriptService(
            api_key=settings.DEEPGRAM_API_KEY, file_name=file_path
        )
        service.run_process()
        await message.answer(
            text=MESSAGES.get('transcription_process_completed')
        )

        document = FSInputFile(
            path=f'{file_path[:-4]}.txt',
            filename=f'{original_filename[:-4]}.txt'
        )
        await bot.send_document(
            chat_id=message.chat.id,
            document=document,
        )
        service.clean_garbage()

    except Exception as e:
        await message.answer(
            text=MESSAGES.get('common_error').format(e)
        )
