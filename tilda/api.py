import os
import requests
from django.conf import settings
from django.utils.timezone import now

from .helpers import download_file, make_unique
from . import models


API_HOST = 'http://api.tildacdn.info/v1'
API_PAYLOAD = {
    'publickey': settings.TILDA_PUBLIC_KEY,
    'secretkey': settings.TILDA_SECRET_KEY
}


def api_getpageslist():
    url = '{}/getpageslist'.format(API_HOST)
    payload = API_PAYLOAD.copy()
    payload['projectid'] = settings.TILDA_PROJECTID
    req = requests.get(url, params=payload)
    if req.status_code == 200:
        res = req.json()
        if res['status'] == 'FOUND':
            for r in res['result']:
                obj, created = models.TildaPage.objects.get_or_create(
                    id=r['id']
                )

                obj.title = r['title']
                obj.save()
            return True
    return False


def api_getpageexport(page_id):
    url = '{}/getpageexport'.format(API_HOST)
    page = models.TildaPage.objects.get(id=page_id)
    payload = API_PAYLOAD.copy()
    payload['pageid'] = page.id
    req = requests.get(url, params=payload)
    if req.status_code == 200:
        res = req.json()
        if res['status'] == 'FOUND':

            """
                Remove old images
            """

            for img in page._path_images_list():
                if os.path.exists(img):
                    os.remove(img)

            """
                Download new images, css, js
            """

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
                download_file(r['from'], filename)
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
    return False
