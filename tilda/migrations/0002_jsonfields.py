from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tilda', '0001_initial'),
    ]

    operations = [
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
