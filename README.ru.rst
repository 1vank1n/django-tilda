Django Tilda
============

`English readme <README.rst>`_

|Downloads|

.. |Downloads| image:: https://pepy.tech/badge/django-tilda
   :target: https://pepy.tech/project/django-tilda

**Внимание!** Перед тем как приступить к интеграции с `tilda.cc`_ убедитесь, что у Вас “Tilda Business” тариф. Только на нём доступно Tilda API.

Синхронизация возможна только для **опубликованных** страниц Проекта.

Поддерживаемые версии
------------------

-  Django >= 2.0 (поддерживаются старые версии >= 1.10)
-  Python 2.7, >= 3.5

Скриншот
-----------

.. figure:: https://img-fotki.yandex.ru/get/518060/94968737.3/0_9cefa_18f3e324_orig
   :alt: Screenshot

   Screenshot

Быстрый старт
-----------------

1. Устанавливаем Django Tilda:

::

    pip install django-tilda

2. Добавь в ``INSTALLED_APPS``:

::

    'django_object_actions',
    'tilda',

3. Также добавь в ``settings.py``:

*TILDA_PUBLIC_KEY* и *TILDA_SECRET_KEY* генерируется на Tilda.cc — https://tilda.cc/identity/apikeys/

*TILDA_PROJECTID* — у Вас должен быть уже созданный проект на Tilda.cc (в адресной строке легко можно найти project_id)

*TILDA_MEDIA_IMAGES_URL* — url до папки TILDA_MEDIA_IMAGES

::

    TILDA_PUBLIC_KEY = ''
    TILDA_SECRET_KEY = ''
    TILDA_PROJECTID = ''
    TILDA_MEDIA_IMAGES_URL = '/media/tilda/images'
    TILDA_MEDIA_IMAGES = os.path.join(BASE_DIR, 'media/tilda/images')
    TILDA_MEDIA_JS = os.path.join(BASE_DIR, 'media/tilda/js')
    TILDA_MEDIA_CSS = os.path.join(BASE_DIR, 'media/tilda/css')

4. *TILDA_MEDIA_IMAGES*, *TILDA_MEDIA_JS*, *TILDA_MEDIA_CSS* — создайте эти папки самостоятельно (это важно!)

5. Запустить миграцию ``python manage.py migrate``

Готово!

Использование
-----

Простой пример:

**models.py**

.. code:: python

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

**template** (``object`` — экземпляр Page class)

.. code:: html

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

Localizations
-------------

-  English
-  Русский

.. _tilda.cc: https://tilda.cc/?r=1614568
