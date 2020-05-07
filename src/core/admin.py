from django.contrib import admin
from .models import NotificationLevel, NotificationTemplate


@admin.register(NotificationLevel)
class NotificationLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'level', 'is_active', 'created', 'modified']
    list_editable = ['is_active']
