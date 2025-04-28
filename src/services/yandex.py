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


def check_file_size(yandex_url: str):
    response = requests.get(
        'https://cloud-api.yandex.net/v1/disk/public/resources',
        params={'public_key': yandex_url, 'fields': 'size'},
        headers={
            'Authorization': f'OAuth {settings.YA_TOKEN}'
        }
    )
    response.raise_for_status()
    file_info = response.json()
    file_size = file_info.get('size')
    if file_size > 1024 * 1024 * 1024:
        return False
    return True
