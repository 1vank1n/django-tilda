import os

from django.test import TestCase

from tilda.models import TildaPage


class TildaPageModelTests(TestCase):
    def test_lists_from_json_fields(self):
        page = TildaPage.objects.create(
            id='1',
            title='Page',
            images=[{'to': 'img.jpg'}],
            css=[{'to': 'style.css'}],
            js=[{'to': 'app.js'}],
        )

        self.assertEqual(
            page.get_images_list(),
            [os.path.join('/media/tilda/images', 'img.jpg')],
        )
        self.assertEqual(
            page.get_css_list(),
            [os.path.join('/media/tilda/css', 'style.css')],
        )
        self.assertEqual(
            page.get_js_list(),
            [os.path.join('/media/tilda/js', 'app.js')],
        )
