# coding: utf-8
import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TildaPage(models.Model):

    id = models.CharField(
        _(u'Page id'),
        max_length=50,
        primary_key=True,
        unique=True
    )

    title = models.CharField(
        _(u'Title'),
        max_length=100
    )

    html = models.TextField(
        _(u'HTML'),
        blank=True
    )

    images = models.TextField(
        _(u'Images'),
        blank=True
    )

    css = models.TextField(
        _(u'CSS'),
        blank=True
    )

    js = models.TextField(
        _(u'JS'),
        blank=True
    )

    synchronized = models.DateTimeField(
        _(u'Synchronized time'),
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        _(u'Created'),
        auto_now_add=True
    )

    class Meta:
        ordering = ('title', )
        verbose_name = _(u'page')
        verbose_name_plural = _(u'Tilda Pages')

    def get_images_list(self):
        if self.images:
            return [
                os.path.join('/media/tilda/images', r['to'])
                for r in eval(self.images)
            ]
        return []

    def get_css_list(self):
        if self.css:
            return [
                os.path.join('/media/tilda/css', r['to'])
                for r in eval(self.css)
            ]
        return []

    def get_js_list(self):
        if self.js:
            return [
                os.path.join('/media/tilda/js', r['to'])
                for r in eval(self.js)
            ]
        return []

    def _path_images_list(self):
        if self.images:
            return [
                os.path.join(settings.TILDA_MEDIA_IMAGES, r['to'])
                for r in eval(self.images)
            ]
        return []

    def _path_css_list(self):
        if self.css:
            return [
                os.path.join(settings.TILDA_MEDIA_CSS, r['to'])
                for r in eval(self.css)
            ]
        return []

    def _path_js_list(self):
        if self.js:
            return [
                os.path.join(settings.TILDA_MEDIA_JS, r['to'])
                for r in eval(self.js)
            ]
        return []

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
