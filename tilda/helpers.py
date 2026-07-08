import logging
import os

import requests

logger = logging.getLogger(__name__)

DOWNLOAD_TIMEOUT = 30
USER_AGENT = (
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'
)


def safe_join(base, relative_path):
    base = os.path.normpath(base)
    path = os.path.normpath(os.path.join(base, relative_path))
    if path != base and not path.startswith(base + os.sep):
        logger.error('Unsafe file path %r skipped', relative_path)
        return None
    return path


def download_file(url, filename):
    headers = {'User-Agent': USER_AGENT}
    try:
        with requests.get(
            url, stream=True, timeout=DOWNLOAD_TIMEOUT, headers=headers
        ) as response:
            response.raise_for_status()
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=8192):
                    fd.write(chunk)
    except (requests.RequestException, OSError) as exc:
        logger.error('Failed to download %s: %s', url, exc)
        return False
    return True


def make_unique(original_list):
    unique_list = []
    for obj in original_list:
        if obj not in unique_list:
            unique_list.append(obj)
    return unique_list
