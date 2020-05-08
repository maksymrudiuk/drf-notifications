from django.contrib.auth import get_user_model
from django.template import Template
from django.template.loader import get_template as django_get_template
from core.utils import reserved_getattr
from .formatters import ContentHTMLFormatter


User = get_user_model()


class TemplateContentMixin:

    template_field = 'template'
    message_field = 'full_message'
    reserve_messege_field = 'short_message'

    def get_template(self) -> Template:

        if self.notification.template:
            return django_get_template(getattr(self.notification, self.template_field))

        template_string = reserved_getattr(
            self.notification,
            self.message_field,
            self.reserve_messege_field
        )

        template = self.validate_template_string(template_string)
        return Template(template)

    def get_content(self, formatter=ContentHTMLFormatter):
        template = self.get_template()
        context = self.get_context()
        content = formatter(template, context)
        return content.render()


# TODO In next release deprecate serializer depencies
class JsonContentMixin:

    serializer_class = None

    def get_serializer_class(self):

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_content(self):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.notification, render_context=self.context)
        return serializer.data
