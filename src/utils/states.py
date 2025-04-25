from aiogram.fsm.state import StatesGroup, State


class FSMTranscriptionStage(StatesGroup):
    local_process_start = State()
    yandex_process_start = State()
    questions_process_start = State()
