import ast
import json

from django.db import migrations, models


def _to_json_text(value):
    """Старые версии хранили Python-repr списка в TextField."""
    if not value:
        return '[]'
    try:
        return json.dumps(ast.literal_eval(value))
    except (ValueError, SyntaxError):
        pass
    try:
        json.loads(value)
        return value
    except (TypeError, ValueError):
        return '[]'


def convert_repr_to_json(apps, schema_editor):
    TildaPage = apps.get_model('tilda', 'TildaPage')
    for page in TildaPage.objects.all().iterator():
        page.images = _to_json_text(page.images)
        page.css = _to_json_text(page.css)
        page.js = _to_json_text(page.js)
        page.save(update_fields=['images', 'css', 'js'])


class Migration(migrations.Migration):

    dependencies = [
        ('tilda', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(convert_repr_to_json, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='tildapage',
            name='images',
            field=models.JSONField(blank=True, default=list, verbose_name='Images'),
        ),
        migrations.AlterField(
            model_name='tildapage',
            name='css',
            field=models.JSONField(blank=True, default=list, verbose_name='CSS'),
        ),
        migrations.AlterField(
            model_name='tildapage',
            name='js',
            field=models.JSONField(blank=True, default=list, verbose_name='JS'),
        ),
    ]
