from .base import ModelNotification
from .mixins import JsonContentMixin


class BasePushNotification(JsonContentMixin, ModelNotification):

    device_queryset = None
    serializer_class = None

    def get_device_queryset(self):
        assert self.device_queryset is not None, (
            "'%s' should either include a `device_queryset` attribute, "
            "or override the `get_device_queryset()` method."
            % self.__class__.__name__
        )

        return self.device_queryset

    def get_filtered_queryset(self, queryset, **kwargs):
        """ Method.
        Provide all custom filters in this method.
        Arguments:
            queryset {queryset} -- device queryset.
        Returns:
            [queryset] -- scoped by kwargs device queryset.
        """

        return queryset.filter(active=True, user__email=self.recipient, **kwargs)

    def create(self, **kwargs):
        """ Method.
        Get all devices for recipient.
        Returns:
            [queryset] -- different user devices in one queryset.
        """

        self.validate_recipient()
        devices = list(device for device in self.get_filtered_queryset(self.get_device_queryset()))

        return devices

    def send(self, **kwargs):
        """ Method."""

        devices = self.create()
        message = self.get_message()
        self.perform_send(devices, message)

    def perform_send(self, devices, content, **kwargs):
        """ Method.
        Arguments:
            devices {queryset} -- device queryset.
            content {dict} -- content to send.
        """

        for device in devices:
            device.send_message(**content)

    def get_message(self):
        return self.get_content()
