import logging
import os

import requests
from django.conf import settings
from django.utils.timezone import now

from .helpers import download_file, make_unique
from . import models


logger = logging.getLogger(__name__)

API_HOST = 'https://api.tildacdn.info/v1'
API_PAYLOAD = {
    'publickey': settings.TILDA_PUBLIC_KEY,
    'secretkey': settings.TILDA_SECRET_KEY
}
API_TIMEOUT = getattr(settings, 'TILDA_TIMEOUT', 10)


def api_getpageslist():
    url = f"{API_HOST}/getpageslist"
    payload = API_PAYLOAD.copy()
    payload['projectid'] = settings.TILDA_PROJECTID
    try:
        req = requests.get(url, params=payload, timeout=API_TIMEOUT)
        req.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Error fetching pages list from Tilda: %s", exc)
        return False

    res = req.json()
    if res.get('status') == 'FOUND':
        for r in res.get('result', []):
            obj, _created = models.TildaPage.objects.get_or_create(
                id=r['id']
            )
            obj.title = r['title']
            obj.save()
        return True
    return False


def api_getpageexport(page_id):
    url = f"{API_HOST}/getpageexport"
    page = models.TildaPage.objects.get(id=page_id)
    payload = API_PAYLOAD.copy()
    payload['pageid'] = page.id
    try:
        req = requests.get(url, params=payload, timeout=API_TIMEOUT)
        req.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Error fetching page export from Tilda: %s", exc)
        return False

    res = req.json()
    if res.get('status') != 'FOUND':
        return False

    # Remove old images
    for img in page._path_images_list():
        if os.path.exists(img):
            os.remove(img)

    # Download new images, css, js
    result = res['result']
    page.title = result['title']
    page.html = result['html']
    page.images = result['images']
    page.css = result['css']
    page.js = result['js']
    page.synchronized = now()
    page.save()

    for r in make_unique(result['images']):
        filename = os.path.join(settings.TILDA_MEDIA_IMAGES, r['to'])
        if download_file(r['from'], filename):
            url = os.path.join(settings.TILDA_MEDIA_IMAGES_URL, r['to'])
            page.html = page.html.replace(r['to'], url)
    page.save()

    for r in make_unique(result['css']):
        filename = os.path.join(settings.TILDA_MEDIA_CSS, r['to'])
        download_file(r['from'], filename)

    for r in make_unique(result['js']):
        filename = os.path.join(settings.TILDA_MEDIA_JS, r['to'])
        download_file(r['from'], filename)

    return True
