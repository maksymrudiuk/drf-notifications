from django.utils.html import strip_tags


class BaseContentFormatter:

    def __init__(self, template, context):
        self.template = template
        self.context = context


class ContentHTMLFormatter(BaseContentFormatter):

    def render(self):
        return self.template.render(self.context)


class ContentTextFormatter(ContentHTMLFormatter):

    def render(self):
        return strip_tags(super(ContentTextFormatter, self).render())
