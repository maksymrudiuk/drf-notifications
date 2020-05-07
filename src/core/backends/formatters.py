from django.utils.html import strip_tags


class BaseContentFormatter:

    def __init__(self, template, context):
        self.template = template
        self.context = context


class ContentHTMLFormatter(BaseContentFormatter):

    def __call__(self):
        return self.template.render(self.context)


class ContentTextFormatter(ContentHTMLFormatter):

    def __call__(self):
        return strip_tags(super(ContentTextFormatter, self).create())
