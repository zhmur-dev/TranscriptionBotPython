import os

from aiogram import Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from urllib.parse import parse_qs, unquote, urlparse

from src.config.config import settings
from src.services.transcription import TranscriptService
from src.messages.yandex_msg import MESSAGES
from src.services.yandex import check_file_size, get_direct_url
from src.utils.states import FSMTranscriptionStage

yandex_router = Router()


@yandex_router.message(Command(commands='yandex'))
async def start_yandex_process(message: Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer(text=MESSAGES.get('paste_link'))
    await state.set_state(FSMTranscriptionStage.yandex_process_start)


@yandex_router.message(
    StateFilter(FSMTranscriptionStage.yandex_process_start)
)
async def handle_yandex_url(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(state=None)

    try:
        download_url = get_direct_url(message.text)
        if not check_file_size(message.text):
            await message.answer(text=MESSAGES.get('file_too_big'))
            return

        parsed_url = urlparse(download_url)
        query_params = parse_qs(parsed_url.query)
        filename_encoded = query_params.get('filename', [None])[0]
        filename = unquote(filename_encoded)

        await message.answer(text=MESSAGES.get('transcription_process'))
        service = TranscriptService(
            api_key=settings.DEEPGRAM_API_KEY,
            yandex_file_path=download_url,
            yandex_file_name=filename,
        )
        service.run_process()
        await message.answer(
            text=MESSAGES.get('transcription_process_completed')
        )

        document = FSInputFile(
            path=os.path.join(
                str(settings.TG_SERVER_PATH),
                settings.BOT_TOKEN,
                settings.TG_SERVER_WORKDIR,
                filename[:-4] + '.txt'
            ),
            filename=f'{filename[:-4]}.txt'
        )
        await bot.send_document(
            chat_id=message.chat.id,
            document=document,
        )

    except Exception as e:
        await message.answer(
            text=MESSAGES.get('common_error').format(e)
        )

    try:
        service.clean_garbage()  # noqa

    except Exception:  # noqa
        pass
