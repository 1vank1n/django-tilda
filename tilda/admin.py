# coding: utf-8
from django.contrib import admin, messages
from django_object_actions import DjangoObjectActions
from django.utils.translation import gettext, gettext_lazy as _

from . import api
from . import models


class TildaPageAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('title', 'id', 'synchronized', 'created', )
    list_filter = ('synchronized', 'created', )
    search_fields = ('title', 'id', )
    readonly_fields = (
        'id',
        'title',
        'html',
        'images',
        'css',
        'js',
        'synchronized',
        'created',
    )

    def has_add_permission(self, request):
        return False

    def fetch_pages(modeladmin, request, queryset):
        if api.api_getpageslist():
            messages.add_message(
                request,
                messages.SUCCESS,
                gettext('Pages successfully fetched from Tilda')
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                gettext('Nothing fetched. Perhaps wrong settings')
            )
    fetch_pages.label = _('Fetch pages')

    def synchronize_page(self, request, obj):
        if api.api_getpageexport(obj.id):
            messages.add_message(
                request,
                messages.SUCCESS,
                gettext('Page «%(title)s» successfully synced from Tilda') % {'title': obj.title}
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                gettext('Something wrong...')
            )
    synchronize_page.label = _('Synchronize')

    change_actions = ('synchronize_page', )
    changelist_actions = ('fetch_pages', )

admin.site.register(models.TildaPage, TildaPageAdmin)
