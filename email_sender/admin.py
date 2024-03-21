from django.contrib import admin
from .models import RecipientGroup, Recipient
from django.contrib.admin import display, register, ModelAdmin


admin.site.site_header = "EXANTE EMAIL SENDER ADMIN"
admin.site.site_title = "EXANTE EMAIL SENDER "
admin.site.index_title = "Manage exante email"


@register(RecipientGroup)
class RecipientGroupAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@register(Recipient)
class RecipientAdmin(ModelAdmin):
    list_display = ['email', '_groups']
    search_fields = ['email']

    @display(description='groups')
    def _groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])
