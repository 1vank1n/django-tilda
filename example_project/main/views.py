from django.views.generic import (TemplateView, DetailView)
from . import models


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_list'] = models.Page.objects.all()
        return context


class PageDetailView(DetailView):
    template_name = 'page.html'
    model = models.Page
