from django import forms
from django.apps import apps
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string


class TildaWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs.setdefault('id', f'id_{name}')
        is_required = self.is_required
        is_need_config = any(
            not getattr(settings, attr, None)
            for attr in ['TILDA_PUBLIC_KEY', 'TILDA_SECRET_KEY', 'TILDA_PROJECTID']
        )

        TildaPage = apps.get_model('tilda', 'TildaPage')
        queryset = TildaPage.objects.all()
        obj = queryset.filter(id=value).first() if queryset and value else None

        context = {
            'is_required': is_required,
            'is_need_config': is_need_config,
            'queryset': queryset,
            'name': name,
            'value': value,
            'attrs': attrs,
            'obj': obj,
        }
        return render_to_string('tilda/widget.html', context)


class TildaPageField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'tilda.TildaPage'
        super(TildaPageField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = TildaWidget
        return super(TildaPageField, self).formfield(**kwargs)
