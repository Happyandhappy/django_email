from django.db import models
from entrances.models import Entrance, Apartment
from nomenclatures.models import TaskType, Priority
from dynamic_costs.models import DynamicCost, ApartmentDynamicCost
from django.utils.translation import ugettext_lazy as _
import select2.fields
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime
from ckeditor.fields import RichTextField
from vhodove.helper import first_day_of_month, last_day_of_month
from smart_selects.db_fields import ChainedForeignKey

class EasyPayLog(models.Model):
    ref = models.CharField(max_length=255, blank=True, null=True)


class Task(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    resolved = models.BooleanField(_('Resolved'), default=False)
    resolved_by_admin = models.BooleanField(_('Resolved by admin'), default=False)
    can_pay = models.BooleanField(_('Can pay'), default=False)
    can_pay_partial = models.BooleanField(_('Can pay partial'), default=False)
    assignee = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True, limit_choices_to={'is_staff': True})
    entrance = select2.fields.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name, blank=True, null=True, limit_choices_to={'active': True})
    apartment = ChainedForeignKey(
        Apartment,
        chained_field="entrance",
        chained_model_field="entrance",
        show_all=False,
        auto_choose=True,
        verbose_name=Apartment._meta.verbose_name,
        blank=True,
        null=True
    )
    task_type = select2.fields.ForeignKey(TaskType, verbose_name=TaskType._meta.verbose_name, limit_choices_to={'active': True})
    priority = select2.fields.ForeignKey(Priority, verbose_name=Priority._meta.verbose_name, limit_choices_to={'active': True})

    price = models.DecimalField(_('Price'), blank=True, null=True, decimal_places=2, max_digits=8)
    partial_paid = models.DecimalField(_('Partial paid'), blank=True, null=True, decimal_places=2, max_digits=8, editable=False)
    partial_paid_total = models.DecimalField(_('Partial paid total'), blank=True, null=True, decimal_places=2, max_digits=8)
    price_for_resolve = models.DecimalField(_('Price for resolve'), blank=True, null=True, decimal_places=2, max_digits=8, editable=False)

    from_date = models.DateField(_('From date'), blank=True, null=True, default=first_day_of_month, editable=False)
    to_date = models.DateField(_('To date'), blank=True, null=True, default=last_day_of_month, editable=False)
    date = models.DateField(_('Month'), blank=True, null=True)

    common_information = RichTextField(_('Common information'), blank=True, null=True)
    dynamic_cost = models.ForeignKey(DynamicCost, blank=True, null=True, editable=False)
    apartment_dynamic_cost = models.ForeignKey(ApartmentDynamicCost, blank=True, null=True, editable=False)
    document = models.FileField(_('Document'), upload_to='maintaskdocuments/%Y/%m', blank=True, null=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    easypay_code = models.CharField(_('Easypay code'), max_length=255, blank=True, null=True)

    def has_easypay(self):
        return self.easypay_code is not Null
    has_easypay.allow_tags = True
    has_easypay.short_description = _('Easypay code')

    def __unicode__(self):
        return self.title


    def get_date(self):
        if self.date:
            return "%s.%s" %(self.date.month, self.date.year)
        else:
            return '-'

    get_date.short_description = _('Month')
    get_date.allow_tags = False
    get_date.admin_order_field = 'date'

    def save(self, *args, **kwargs):
        self.can_pay = self.task_type.can_pay
        self.can_pay_partial = self.task_type.can_pay_partial
        self.price_for_resolve = self.task_type.price_for_resolve

        self.from_date = first_day_of_month(self.date)
        self.to_date = last_day_of_month(self.date)
        super(Task, self).save(*args, **kwargs)

        if self.apartment_dynamic_cost:
            self.apartment_dynamic_cost.is_paid = self.resolved
            self.apartment_dynamic_cost.price = self.price
            self.apartment_dynamic_cost.save()

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ('apartment__floor', 'apartment__apartment_integer',)


class PartialTaskPay(models.Model):
    assignee = models.ForeignKey(User, verbose_name=_('User'), limit_choices_to={'is_staff': True})
    task = models.ForeignKey(Task)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    easypay_code = models.CharField(_('Easypay code'), max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(PartialTaskPay, self).save(*args, **kwargs)

        if self.task.task_type.can_pay_partial:
            cnt = PartialTaskPay.objects.filter(task=self.task).aggregate(Sum('price'))
            self.task.partial_paid_total = cnt.get('price__sum')
            if self.task.partial_paid_total == self.task.price:
                self.task.resolved = True
            self.task.save()

    def delete(self, *args, **kwargs):
        super(PartialTaskPay, self).delete(*args, **kwargs)
        if self.task.task_type.can_pay_partial:
            cnt = PartialTaskPay.objects.filter(task=self.task).aggregate(Sum('price'))
            self.task.partial_paid_total = cnt.get('price__sum')
            self.task.save()

    class Meta:
        verbose_name = _('task partial pay')
        verbose_name_plural = _('task partial pays')
        ordering = ('created_at',)

    def __unicode__(self):
        return '#'


class TaskDocument(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    document = models.FileField(_('Document'), upload_to='taskdocuments/%Y/%m')

    task = models.ForeignKey(Task, verbose_name=Task._meta.verbose_name)

    def file_link(self):
        if self.document:
            return "<a href='%s'>%s</a>" % (self.document.url, self.document.url.rsplit('/', 1)[1])
        else:
            return "-"
    file_link.allow_tags = True
    file_link.short_description = _('file link')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('uploaded document')
        verbose_name_plural = _('uploaded documents')


class Schedule(models.Model):
    entrance = select2.fields.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name, blank=True, null=True, limit_choices_to={'active': True})
    assignee = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True, limit_choices_to={'is_staff': True})
    from_date = models.DateField(_('From date'), default=first_day_of_month)
    to_date = models.DateField(_('To date'), default=last_day_of_month)
    visit_date = models.DateField(_('Visit date'), default=datetime.date.today)
    is_cachier = models.BooleanField(_('Is real cachier'), default=False)

    def __unicode__(self):
        return "%s | %s %s | (%s-%s)" % (self.entrance.title, self.assignee.first_name, self.assignee.last_name, self.from_date, self.to_date)

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        ordering = ('visit_date',)


class PaymentAhead(models.Model):
    entrance = select2.fields.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name, limit_choices_to={'active': True})
    apartment = ChainedForeignKey(
        Apartment,
        chained_field="entrance",
        chained_model_field="entrance",
        show_all=False,
        auto_choose=True,
        verbose_name=Apartment._meta.verbose_name,
    )
    assignee = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True, editable=False, limit_choices_to={'is_staff': True})
    from_date = models.DateField(_('From date'))

    period = models.IntegerField(_('Period'))

    def save(self, *args, **kwargs):
        self.from_date = datetime.date(self.from_date.year, self.from_date.month, 1)
        super(PaymentAhead, self).save(*args, **kwargs)
        task_type_fee = TaskType.objects.get(default_fee=True)
        for i in range(0, self.period):
            y = self.from_date.year
            m = self.from_date.month + i
            if m > 12:
                m = m - 12
                y = y+1
            period_from_date = first_day_of_month(datetime.date(y, m, 1))
            period_to_date = last_day_of_month(datetime.date(y, m, 1))

            if not Task.objects.filter(task_type=task_type_fee, entrance=self.entrance, apartment=self.apartment, from_date= period_from_date, to_date=period_to_date).exists():
                t = Task()
                t.title = '%s %s' % ('[*]', task_type_fee.title)
                t.task_type = task_type_fee
                t.priority = Priority.objects.get(default=True)
                t.entrance = self.entrance
                t.apartment = self.apartment
                t.from_date = period_from_date
                t.date = period_from_date
                t.resolved = True
                t.to_date = period_to_date
                t.assignee = self.assignee
                t.price = self.apartment.monthly_fee
                t.save()

    class Meta:
        verbose_name = _('PaymentAhead')
        verbose_name_plural = _('PaymentAhead')
        ordering = ('from_date',)
