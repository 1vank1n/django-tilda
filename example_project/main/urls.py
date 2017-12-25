from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),

    url(r'^(?P<pk>[-\w]+)/$',
        views.PageDetailView.as_view(),
        name='page_detail'),
]
