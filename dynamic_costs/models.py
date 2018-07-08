from django.db import models
from entrances.models import Entrance, Apartment
from nomenclatures.models import TaskType, Priority
from django.utils.translation import ugettext_lazy as _
import select2.fields
from django.db.models import signals
from ckeditor.fields import RichTextField
from vhodove.helper import first_day_of_month, last_day_of_month


class DynamicCost(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    task_type = select2.fields.ForeignKey(TaskType, verbose_name=TaskType._meta.verbose_name, limit_choices_to={'active': True})
    priority = select2.fields.ForeignKey(Priority, verbose_name=Priority._meta.verbose_name, limit_choices_to={'active': True})
    price = models.DecimalField(_('Price'), blank=True, null=True, decimal_places=2, max_digits=8, help_text=_('For entire entrance'))
    from_date = models.DateField(_('From date'), default=first_day_of_month)
    to_date = models.DateField(_('To date'), default=last_day_of_month)
    entrance = select2.fields.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name, limit_choices_to={'active': True})
    active = models.BooleanField(_('Active'), default=True)
    common_information = RichTextField(_('Common information'), blank=True, null=True)
    apartments = select2.fields.ManyToManyField(Apartment, verbose_name=Apartment._meta.verbose_name_plural, through='ApartmentDynamicCost')

    def __unicode__(self):
        return self.title

    def get_priority(self):
        return '<span style="background:%s;display:block;width:22px;height:22px;"></span>' % (self.priority.color)

    get_priority.short_description = ''
    get_priority.allow_tags = True

    class Meta:
        verbose_name = _('Dynamic cost')
        verbose_name_plural = _('Dynamic costs')


class ApartmentDynamicCost(models.Model):
    apartment = models.ForeignKey(Apartment, verbose_name=Apartment._meta.verbose_name)
    cost = models.ForeignKey(DynamicCost, verbose_name=Apartment._meta.verbose_name)
    price = models.DecimalField(_('Price'), blank=True, null=True, decimal_places=2, max_digits=8)
    is_paid = models.BooleanField(_('Is paid'), default=False)

    def __unicode__(self):
        return self.apartment.__unicode__()

    class Meta:
        ordering = ('apartment__floor', 'apartment__apartment_integer',)
        verbose_name = _('Apartment dynamic cost')
        verbose_name_plural = _('Apartment dynamic costs')


def add_apartment_dynamic_costs(sender, instance, created, **kwargs):
    if created:
        if instance.task_type.can_pay:
            for item in instance.entrance.apartment_set.all():
                ApartmentDynamicCost(cost=instance, apartment=item).save()

        else:
            from tasks.models import Task
            t = Task()
            t.title = instance.title
            t.task_type = instance.task_type
            t.priority = instance.priority
            t.entrance = instance.entrance
            t.from_date = instance.from_date
            t.to_date = instance.to_date
            t.price = instance.price
            t.dynamic_cost = instance
            t.save()

signals.post_save.connect(add_apartment_dynamic_costs, sender=DynamicCost)
