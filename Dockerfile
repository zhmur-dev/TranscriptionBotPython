FROM python:3.13-slim

WORKDIR /transcription_efmobot

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["/bin/bash", "-c", "python3 aiogram_run.py"]