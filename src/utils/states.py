from aiogram.fsm.state import StatesGroup, State


class FSMTranscriptionStage(StatesGroup):
    transcription_run = State()
    managing_questions = State()
    correct_question = State()
