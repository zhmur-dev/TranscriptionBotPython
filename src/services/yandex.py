import requests

from src.config.config import settings
from src.messages.yandex_msg import MESSAGES


class DeadLinkException(Exception):
    pass


def get_direct_url(yandex_url: str) -> str:  # noqa
    url = settings.yandex_cloud_api_url.format(yandex_url)
    response = requests.get(url)
    if not response:
        raise DeadLinkException(MESSAGES.get('link_error', ''))
    download_url = response.json().get('href')
    return download_url
