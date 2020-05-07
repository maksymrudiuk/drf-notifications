from django.contrib import admin
from .models import NotificationLevel, NotificationTemplate


@admin.register(NotificationLevel)
class NotificationLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    pass
