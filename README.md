### TranscriptionBotPython

A simple audio/video transcription Telegram bot using Deepgram as AI assistant. It can transcribe either local files received via bot interface, or remote files from Yandex Disk via public URL.

#### Installation and startup

- Clone the repository

```commandline
git clone https://github.com/zhmur-dev/TranscriptionBotPython.git
```

- Set up a `creds/.env` file as suggested in `.env.example`
- Run it in a Docker container

```commandline
docker compose up --build
```

Make sure you have Docker installed on your server.