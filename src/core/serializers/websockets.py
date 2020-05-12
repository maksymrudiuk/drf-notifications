from collections import OrderedDict

from rest_framework import serializers

from .mixins import RenderSerializerMixin


class BaseNotificationLevelSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return OrderedDict({
            "name": instance.name,
            "priority": instance.get_priority_display()
        })


# TODO Create render fields istead RenderSerializerMixin
class WebSocketNotificationSerializer(RenderSerializerMixin, serializers.BaseSerializer):

    def to_representation(self, instance):

        level_serializer = BaseNotificationLevelSerializer(instance.level)

        return OrderedDict({
            "name": instance.name,
            "level": level_serializer.data,
            "subject": self.render_content(instance.subject),
            "message": self.render_content(instance.short_message)
        })
