from django.utils.html import strip_tags
from django.template import Context, Template

from rest_framework.fields import empty

from core.backends.utils import validate_template_string


class RenderSerializerMixin:

    def __init__(self, instance=None, data=empty, render_context={}, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.render_context = render_context

    def render_content(self, template):
        template_string = validate_template_string(template, (('\n', ''), ('&nbsp;', '')))
        template = Template(template_string)
        context = Context(self.render_context)

        return strip_tags(template.render(context))
