from django import forms
from django.apps import apps
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string


class TildaWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        attrs = dict(attrs or {})
        attrs.setdefault('id', 'id_{}'.format(name))

        is_need_config = any(
            not getattr(settings, key, None)
            for key in ('TILDA_PUBLIC_KEY', 'TILDA_SECRET_KEY', 'TILDA_PROJECTID')
        )

        TildaPage = apps.get_model('tilda', 'TildaPage')
        queryset = TildaPage.objects.all()
        obj = queryset.filter(id=value).first() if value else None

        context = {
            'name': name,
            'value': value,
            'attrs': attrs,
            'is_required': self.is_required,
            'is_need_config': is_need_config,
            'queryset': queryset,
            'obj': obj,
        }
        return render_to_string('tilda/widget.html', context)


class TildaPageField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'tilda.TildaPage'
        kwargs.setdefault('on_delete', models.CASCADE)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = TildaWidget
        return super().formfield(**kwargs)
