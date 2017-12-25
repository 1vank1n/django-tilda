from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.apps import apps


class TildaWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        is_required = self.is_required

        if not hasattr(settings, 'TILDA_PUBLIC_KEY') or \
           not hasattr(settings, 'TILDA_SECRET_KEY') or \
           not hasattr(settings, 'TILDA_PROJECTID') or \
           not settings.TILDA_PUBLIC_KEY or \
           not settings.TILDA_SECRET_KEY or \
           not settings.TILDA_PROJECTID:
            is_need_config = True

        TildaPage = apps.get_model('tilda', 'TildaPage')
        queryset = TildaPage.objects.all()

        if queryset and value:
            obj = queryset.filter(id=value)[0]
        return render_to_string('tilda/widget.html', locals())


class TildaPageField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'tilda.TildaPage'
        super(TildaPageField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = TildaWidget
        return super(TildaPageField, self).formfield(**kwargs)
