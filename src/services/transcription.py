import os
import logging

from deepgram import (  # noqa
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from src.config.config import settings
from src.messages.transcription_msg import MESSAGES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'  # noqa
)


class TranscriptService:
    def __init__(
            self,
            api_key: str,
            tg_file_path: str = None,
            yandex_file_path: str = None,
            yandex_file_name: str = None,
    ):
        self.api_key = api_key
        self.transcription_options = PrerecordedOptions(
            model='nova-2',
            smart_format=True,
            language='ru',
        )
        self.tg_file_path = tg_file_path
        self.yandex_file_path = yandex_file_path
        self.yandex_file_name = yandex_file_name
        self.text_file_name = None


    def _transcribe_file(self):
        logging.info(
            MESSAGES.get('transcription_started')
        )
        try:
            deepgram = DeepgramClient(api_key=self.api_key)
            if not self.yandex_file_path:
                with open(f'{self.tg_file_path}', 'rb') as file:
                    buffer_data = file.read()
                    payload: FileSource = {
                        'buffer': buffer_data,
                    }
                    response = deepgram.listen.rest.v('1').transcribe_file(
                        payload,
                        self.transcription_options,
                        timeout=99999
                    )
            else:
                payload: dict = {'url': self.yandex_file_path}
                response = deepgram.listen.rest.v('1').transcribe_url(
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
        if not self.yandex_file_path:
            self.text_file_name = f'{self.tg_file_path[:-4]}.txt'
        else:
            self.text_file_name = os.path.join(
                str(settings.TG_SERVER_PATH),
                settings.BOT_TOKEN,
                settings.TG_SERVER_WORKDIR,
                self.yandex_file_name[:-4] + '.txt'
            )
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
            if not self.yandex_file_path:
                os.remove(self.tg_file_path)
            os.remove(self.text_file_name)
            logging.info(
                MESSAGES.get('file_deletion_success')
            )
        except Exception as e:
            logging.error(
                MESSAGES.get('file_deletion_error').format(e)
            )
