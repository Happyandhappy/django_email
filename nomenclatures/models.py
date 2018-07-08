from django.db import models
from django.utils.translation import ugettext_lazy as _
from colorful.fields import RGBColorField


class TaskType(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    price_for_resolve = models.DecimalField(_('Price for resolve'), blank=True, null=True, decimal_places=2, max_digits=8)
    can_pay = models.BooleanField(_('Can pay'), default=False, help_text=_('Can pay description'))
    can_pay_partial = models.BooleanField(_('Can pay partial'), default=False)
    for_cachiers = models.BooleanField(_('For cachiers'), default=False, help_text=_('For cachiers description'))
    default_fee = models.BooleanField(_('Default fee'), default=False, help_text=_('Default fee description'))
    home_manager_fee = models.BooleanField(_('Home manager fee'), default=False, help_text=_('Home manager fee description'))
    is_administrative = models.BooleanField(_('Administrative Task'), default=False)
    active = models.BooleanField(_('Active'), default=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(TaskType, self).save(*args, **kwargs)

        if self.default_fee is True:
            TaskType.objects.exclude(id=self.id).update(default_fee=False)

        if self.home_manager_fee is True:
            TaskType.objects.exclude(id=self.id).update(home_manager_fee=False)

    class Meta:
        verbose_name = _('Task type')
        verbose_name_plural = _('Task types')
        ordering = ('title',)


class Priority(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    color = RGBColorField(_('Color'), max_length=255)
    default = models.BooleanField(_('Default'), default=False)
    active = models.BooleanField(_('Active'), default=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Priority, self).save(*args, **kwargs)

        if self.default is True:
            Priority.objects.exclude(id=self.id).update(default=False)

    class Meta:
        verbose_name = _('Priority')
        verbose_name_plural = _('Priorities')
