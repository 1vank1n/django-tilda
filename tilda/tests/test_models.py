from django.test import TestCase

from tilda.models import TildaPage


class TildaPageModelTests(TestCase):
    def test_lists_from_json_fields(self):
        page = TildaPage.objects.create(
            id='100',
            title='Page',
            images=[{'from': 'http://x/img.jpg', 'to': 'img.jpg'}],
            css=[{'from': 'http://x/style.css', 'to': 'style.css'}],
            js=[{'from': 'http://x/app.js', 'to': 'app.js'}],
        )

        self.assertEqual(page.get_images_list(), ['/media/tilda/images/img.jpg'])
        self.assertEqual(page.get_css_list(), ['/media/tilda/css/style.css'])
        self.assertEqual(page.get_js_list(), ['/media/tilda/js/app.js'])

    def test_empty_fields(self):
        page = TildaPage.objects.create(id='101', title='Empty')

        self.assertEqual(page.get_images_list(), [])
        self.assertEqual(page.get_css_list(), [])
        self.assertEqual(page.get_js_list(), [])
        self.assertEqual(str(page), 'Empty')
