from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.template import Context, Template
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
