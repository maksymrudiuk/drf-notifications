from django.urls import re_path
from core.consumers import NotificationConsumer

websoket_urlpatterns = [
    re_path(r'ws/service/notifications/', NotificationConsumer)
]
