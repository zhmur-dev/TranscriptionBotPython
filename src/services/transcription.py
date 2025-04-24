import os
import logging

from deepgram import (  # noqa
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from src.messages.transcription_msg import MESSAGES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'  # noqa
)


class TranscriptService:
    def __init__(self, api_key: str, file_name: str):
        self.api_key = api_key
        self.audio_file_name = file_name
        self.text_file_name = f'{file_name[:-4]}.txt'
        self.base_url = os.getcwd()
        self.transcription_options = PrerecordedOptions(
            model='nova-2',
            smart_format=True,
            language='ru',
        )


    def _transcribe_file(self):
        logging.info(
            MESSAGES.get('transcription_started').format(self.audio_file_name)
        )
        try:
            deepgram = DeepgramClient(api_key=self.api_key)
            with open(f'{self.audio_file_name}', 'rb') as file:
                buffer_data = file.read()
            payload: FileSource = {
                'buffer': buffer_data,
            }
            response = deepgram.listen.rest.v('1').transcribe_file(
                payload,
                self.transcription_options,
                timeout=99999
            )
            result = response.to_dict(
            )['results']['channels'][0]['alternatives'][0]['transcript']
            return result

        except Exception as e:
            logging.error(
                MESSAGES.get('transcription_error').format(e)
            )


    def _create_text_file(self, text_data: str) -> None:
        logging.info(
            MESSAGES.get('saving_transcribed_text').format(self.text_file_name)
        )

        with open(f'{self.text_file_name}', 'w', encoding='utf8') as file:
            file.write(text_data)

        logging.info(
            MESSAGES.get(
                'formatting_transcribed_text').format(self.text_file_name)
        )

        try:
            with open(f'{self.text_file_name}', 'r', encoding='utf8') as file:
                file_data = file.read()

            sentences = file_data.replace(
                '. ', '.\n'
            ).replace(
                '! ', '!\n'
            ).replace(
                '? ', '?\n'
            )

            with open(f'{self.text_file_name}', 'w', encoding='utf8') as file:
                file.write(sentences)

        except Exception as e:
            logging.error(
                MESSAGES.get('file_processing_error').format(e)
            )


    def run_process(self) -> None:
        try:
            text = self._transcribe_file()
            self._create_text_file(text)
        except Exception as e:
            logging.error(
                MESSAGES.get('file_processing_error').format(e)
            )


    def clean_garbage(self) -> None:
        try:
            os.remove(self.audio_file_name)
            os.remove(self.text_file_name)
            logging.info(
                MESSAGES.get('file_deletion_success')
            )
        except Exception as e:
            logging.error(
                MESSAGES.get('file_deletion_error').format(e)
            )
