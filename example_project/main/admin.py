from django.contrib import admin
from . import models


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'tilda_content', 'created', )
    list_filter = ('created', )
    readonly_fields = ('created', )
    search_fields = ('title', )
admin.site.register(models.Page, PageAdmin)
