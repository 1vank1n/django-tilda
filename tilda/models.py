import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TildaPage(models.Model):

    id = models.CharField(
        _('Page id'),
        max_length=50,
        primary_key=True,
        unique=True
    )

    title = models.CharField(
        _('Title'),
        max_length=100
    )

    html = models.TextField(
        _('HTML'),
        blank=True
    )

    images = models.JSONField(
        _('Images'),
        blank=True,
        default=list
    )

    css = models.JSONField(
        _('CSS'),
        blank=True,
        default=list
    )

    js = models.JSONField(
        _('JS'),
        blank=True,
        default=list
    )

    synchronized = models.DateTimeField(
        _('Synchronized time'),
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        _('Created'),
        auto_now_add=True
    )

    class Meta:
        ordering = ('title', )
        verbose_name = _('page')
        verbose_name_plural = _('Tilda Pages')

    def get_images_list(self):
        url = getattr(settings, 'TILDA_MEDIA_IMAGES_URL', '/media/tilda/images')
        return [os.path.join(url, r['to']) for r in self.images or []]

    def get_css_list(self):
        url = getattr(settings, 'TILDA_MEDIA_CSS_URL', '/media/tilda/css')
        return [os.path.join(url, r['to']) for r in self.css or []]

    def get_js_list(self):
        url = getattr(settings, 'TILDA_MEDIA_JS_URL', '/media/tilda/js')
        return [os.path.join(url, r['to']) for r in self.js or []]

    def _path_images_list(self):
        return [
            os.path.join(settings.TILDA_MEDIA_IMAGES, r['to'])
            for r in self.images or []
        ]

    def _path_css_list(self):
        return [
            os.path.join(settings.TILDA_MEDIA_CSS, r['to'])
            for r in self.css or []
        ]

    def _path_js_list(self):
        return [
            os.path.join(settings.TILDA_MEDIA_JS, r['to'])
            for r in self.js or []
        ]

    def __str__(self):
        return self.title
