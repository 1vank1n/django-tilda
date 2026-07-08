from unittest import mock

import requests
from django.test import TestCase, override_settings

from tilda import api
from tilda.models import TildaPage


def _response(json_data, status_code=200):
    response = mock.Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    response.raise_for_status = mock.Mock()
    if status_code >= 400:
        response.raise_for_status.side_effect = requests.HTTPError()
    return response


@override_settings(TILDA_PUBLIC_KEY='pub', TILDA_SECRET_KEY='sec', TILDA_PROJECTID='1')
class ApiGetPagesListTests(TestCase):
    @mock.patch('tilda.api.requests.get')
    def test_creates_and_updates_pages(self, mock_get):
        TildaPage.objects.create(id='1', title='Old title')
        mock_get.return_value = _response({
            'status': 'FOUND',
            'result': [
                {'id': '1', 'title': 'New title'},
                {'id': '2', 'title': 'Second'},
            ],
        })

        self.assertTrue(api.api_getpageslist())
        self.assertEqual(TildaPage.objects.count(), 2)
        self.assertEqual(TildaPage.objects.get(id='1').title, 'New title')

        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith('https://'))
        self.assertIn('timeout', kwargs)

    @mock.patch('tilda.api.requests.get')
    def test_request_error_returns_false(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()
        self.assertFalse(api.api_getpageslist())

    @mock.patch('tilda.api.requests.get')
    def test_not_found_returns_false(self, mock_get):
        mock_get.return_value = _response({'status': 'ERROR'})
        self.assertFalse(api.api_getpageslist())


@override_settings(TILDA_PUBLIC_KEY='pub', TILDA_SECRET_KEY='sec', TILDA_PROJECTID='1')
class ApiGetPageExportTests(TestCase):
    def setUp(self):
        self.page = TildaPage.objects.create(id='1', title='Old')

    @mock.patch('tilda.api.download_file', return_value=True)
    @mock.patch('tilda.api.requests.get')
    def test_export_saves_page_and_rewrites_html(self, mock_get, mock_download):
        mock_get.return_value = _response({
            'status': 'FOUND',
            'result': {
                'title': 'Exported',
                'html': '<img src="img.jpg">',
                'images': [{'from': 'http://x/img.jpg', 'to': 'img.jpg'}],
                'css': [{'from': 'http://x/style.css', 'to': 'style.css'}],
                'js': [{'from': 'http://x/app.js', 'to': 'app.js'}],
            },
        })

        self.assertTrue(api.api_getpageexport('1'))

        self.page.refresh_from_db()
        self.assertEqual(self.page.title, 'Exported')
        self.assertIn('/media/tilda/images/img.jpg', self.page.html)
        self.assertIsNotNone(self.page.synchronized)
        self.assertEqual(mock_download.call_count, 3)

    @mock.patch('tilda.api.download_file', return_value=True)
    @mock.patch('tilda.api.requests.get')
    def test_unsafe_paths_are_skipped(self, mock_get, mock_download):
        mock_get.return_value = _response({
            'status': 'FOUND',
            'result': {
                'title': 'Exported',
                'html': '',
                'images': [{'from': 'http://x/evil', 'to': '../../evil.jpg'}],
                'css': [],
                'js': [],
            },
        })

        self.assertTrue(api.api_getpageexport('1'))
        mock_download.assert_not_called()

    @mock.patch('tilda.api.requests.get')
    def test_request_error_returns_false(self, mock_get):
        mock_get.side_effect = requests.Timeout()
        self.assertFalse(api.api_getpageexport('1'))
