from collections import OrderedDict

from rest_framework import serializers

from .mixins import RenderSerializerMixin


class FCMNotificationSerializer(RenderSerializerMixin, serializers.BaseSerializer):

    def to_representation(self, instance):
        return OrderedDict({
            "title": self.render_message(instance.subject),
            "body": self.render_message(instance.message)
        })
