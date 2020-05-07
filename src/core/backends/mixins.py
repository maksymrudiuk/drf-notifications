from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.template.loader import get_template as django_get_template
from .formatters import ContentHTMLFormatter, ContentTextFormatter


User = get_user_model()


class TemplateContentMixin:

    def get_context(self) -> Context:
        if self.context and isinstance(self.context, (dict, OrderedDict)):
            if self.notification.template:
                return self.context
            return Context(self.context)
        else:
            raise TypeError("Context must be a dict.")

    def get_template(self) -> Template:
        if self.notification.template:
            return django_get_template(self.notification.template)
        return Template(self.notification.message)

    def get_content(self, formatter=ContentHTMLFormatter):
        template = self.get_template()
        context = self.get_context()
        return formatter(template, context)
