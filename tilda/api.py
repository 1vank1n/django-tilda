import logging
import os

import requests
from django.conf import settings
from django.utils.timezone import now

from . import models
from .helpers import download_file, make_unique, safe_join

logger = logging.getLogger(__name__)

API_HOST = 'https://api.tildacdn.info/v1'


def _api_get(method, **params):
    payload = {
        'publickey': settings.TILDA_PUBLIC_KEY,
        'secretkey': settings.TILDA_SECRET_KEY,
    }
    payload.update(params)
    timeout = getattr(settings, 'TILDA_TIMEOUT', 10)
    try:
        response = requests.get(
            '{}/{}'.format(API_HOST, method), params=payload, timeout=timeout
        )
        response.raise_for_status()
        res = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.error('Tilda API %s request failed: %s', method, exc)
        return None
    if res.get('status') != 'FOUND':
        logger.error('Tilda API %s returned status %r', method, res.get('status'))
        return None
    return res.get('result')


def api_getpageslist():
    result = _api_get('getpageslist', projectid=settings.TILDA_PROJECTID)
    if result is None:
        return False
    for r in result:
        models.TildaPage.objects.update_or_create(
            id=r['id'],
            defaults={'title': r['title']},
        )
    return True


def api_getpageexport(page_id):
    page = models.TildaPage.objects.get(id=page_id)
    result = _api_get('getpageexport', pageid=page.id)
    if result is None:
        return False

    for img in page._path_images_list():
        if os.path.exists(img):
            os.remove(img)

    page.title = result['title']
    page.html = result['html']
    page.images = result['images']
    page.css = result['css']
    page.js = result['js']
    page.synchronized = now()

    for r in make_unique(result['images']):
        filename = safe_join(settings.TILDA_MEDIA_IMAGES, r['to'])
        if filename and download_file(r['from'], filename):
            url = os.path.join(settings.TILDA_MEDIA_IMAGES_URL, r['to'])
            page.html = page.html.replace(r['to'], url)
    page.save()

    for r in make_unique(result['css']):
        filename = safe_join(settings.TILDA_MEDIA_CSS, r['to'])
        if filename:
            download_file(r['from'], filename)

    for r in make_unique(result['js']):
        filename = safe_join(settings.TILDA_MEDIA_JS, r['to'])
        if filename:
            download_file(r['from'], filename)

    return True
