Django Tilda
============

**Warning!** Before start you have to register in [tilda.cc](https://tilda.cc/?r=1614568) and have "Tilda Business" account for use Tilda API.

## Supported versions

* Django 1.10, 1.11 (other version yet not tested)
* Python 3 (3.4, 3.5, 3.6)

## Screenshots

![Screenshot](https://img-fotki.yandex.ru/get/518060/94968737.3/0_9cefa_18f3e324_orig)


## Quick-Start Guide

1. Install Django Tilda:

```
pip install django-tilda
```

2. Add to your `INSTALLED_APPS`:

```
'django_object_actions',
'tilda',
```

3. Add in `settings.py` params:

*TILDA_PUBLIC_KEY* and *TILDA_SECRET_KEY* generated in Business account Tilda.cc — https://tilda.cc/identity/apikeys/

*TILDA_PROJECTID* — you need to have exist project in Tilda.cc (look at your location bar when you work with project in Tilda panel)

```
TILDA_PUBLIC_KEY = ''
TILDA_SECRET_KEY = ''
TILDA_PROJECTID = ''
TILDA_MEDIA_IMAGES = os.path.join(BASE_DIR, 'media/tilda/images')
TILDA_MEDIA_JS = os.path.join(BASE_DIR, 'media/tilda/js')
TILDA_MEDIA_CSS = os.path.join(BASE_DIR, 'media/tilda/css')
```

4. *TILDA_MEDIA_IMAGES*, *TILDA_MEDIA_JS*, *TILDA_MEDIA_CSS* — create this folders manually

5. Migrate `python manage.py migrate`

Done!


## Usage

Simple example:

**models.py**

```python
from django.db import models
from tilda import TildaPageField


class Page(models.Model):

    title = models.CharField(
        u'Title',
        max_length=100
    )

    tilda_content = TildaPageField(
        verbose_name=u'Tilda Page'
    )

    created = models.DateTimeField(
        u'Created',
        auto_now_add=True
    )
```


**template** (`object` — instance of Page class)

```html
<head>
    ...
    {% for css in object.tilda_content.get_css_list %}
        <link rel="stylesheet" href="{{ css }}">
    {% endfor %}
    ...
</head>

<body>
    ...
    {{ object.tilda_content.html|safe }}
    ...
    {% for js in object.tilda_content.get_js_list %}
        <script src="{{ js }}"></script>
    {% endfor %}
</body>
```

## Localizations

* English
* Русский