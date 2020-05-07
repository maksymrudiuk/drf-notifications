# ---------------------------- Django imports ------------------------------- #
# Django db
from django.db import models
# Django contrib
from django.contrib.auth import get_user_model
# Django utils
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
# ------------------------ Third-party imports ------------------------------ #
# CKeditor
from ckeditor.fields import RichTextField
# Model utils
from model_utils import Choices
from model_utils.models import TimeStampedModel
# -------------------------- App local imports ------------------------------ #

User = get_user_model()


class NotificationLevel(models.Model):
    """[summary]

    Model class describe notification level
    """

    PRIORITIES = Choices(
        (1, 'low', _('Low')),
        (2, 'normal', _('Normal')),
        (3, 'high', _('High')))

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        default=str)
    slug = models.SlugField(
        verbose_name=_('Slug name'),
        max_length=255)
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'),
        choices=PRIORITIES,
        default=PRIORITIES.normal)
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        blank=True,
        default=True)

    class Meta:
        verbose_name = _('Notification level')
        verbose_name_plural = _('Notification levels')

    def __str__(self):
        return "{} - {}".format(self.name, self.get_priority_display())


class NotificationTemplate(TimeStampedModel):
    """[summary]
        TimeStampedModel {[model]} -- provide <created> and <modified> DateTime fields
    """

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        default=str
    )
    slug = models.SlugField(
        verbose_name=_('Slug name'),
        max_length=255,
    )
    level = models.ForeignKey(
        'core.NotificationLevel',
        verbose_name=_('Level'),
        related_name='notifications',
        default=None,
        on_delete=models.SET_DEFAULT
    )
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        blank=True,
        default=True
    )
    subject = RichTextField(
        verbose_name=_('Subject'),
        max_length=300,
        default=str
    )
    short_message = RichTextField(
        verbose_name=_('Short message'),
        max_length=500,
        default=str,
        help_text=_('Use for Firebase/Runtime messages')
    )
    full_message = RichTextField(
        verbose_name=_('Full message'),
        blank=True,
        default=str
    )
    template = models.CharField(
        verbose_name=_('Template path'),
        max_length=255,
        blank=True,
        default=str,
        help_text=_('If defined use istead full_message')
    )

    class Meta:
        verbose_name = _('Notification template')
        verbose_name_plural = _('Notification templates')

    def __str__(self):
        return "{} - {}/{}".format(self.name, self.level_name, self.level_priority)

    @cached_property
    def level_name(self):
        if self.level:
            return self.level.name
        return ""

    @cached_property
    def level_priority(self):
        if self.level:
            return self.level.get_priority_display()
        return ""
