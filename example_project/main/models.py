from django.db import models
from django.urls import reverse
from tilda import TildaPageField


class Page(models.Model):

    title = models.CharField(
        'Title',
        max_length=100
    )

    tilda_content = TildaPageField(
        verbose_name='Tilda Page'
    )

    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )

    def get_absolute_url(self):
        return reverse('main:page_detail', kwargs={'pk': self.pk})
