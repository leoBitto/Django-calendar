# admin.py

from django.contrib import admin
from .models import EventLink

@admin.register(EventLink)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'object_date',
        'content_type',
        'object_id', 
        'content_object'
        ]
