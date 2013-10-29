from django.contrib import admin

from .models import CustomField

class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('content_type','name')
    list_filter = ('content_type',)
    search_fields = ('content_type__name','name')
import sys
if not 'test' in sys.argv: # Need to register differently in test
    admin.site.register(CustomField, CustomFieldAdmin)
