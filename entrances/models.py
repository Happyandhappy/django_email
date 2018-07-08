from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from nomenclatures.models import TaskType
from ckeditor.fields import RichTextField
import select2.fields
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum, Count
import re


class Entrance(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    position = models.IntegerField(_('Position'), blank=True, null=True, editable=False)
    google_maps = models.URLField(_('Google maps'), max_length=2048, blank=True, null=True)
    tax_form = RichTextField(_('Tax form'), blank=True, null=True)
    tax_amount = models.DecimalField(_('Tax amount'), blank=True, null=True, decimal_places=2, max_digits=8, help_text=_('Tax amount description'))
    contract_date = models.DateField(_('Contract date'),)
    protocol_date = models.DateField(_('Protocol date'),)
    common_information = RichTextField(_('Common information'), blank=True, null=True)
    active = models.BooleanField(_('Active'), default=True)
    dont_sent_emails = models.BooleanField(_('Dont send notification emails'), default=False)
    auto_assign_monthly_tasks = models.BooleanField(_('Auto Assign Monthly Tasks'), default=True)
    monthly_expences = select2.fields.ManyToManyField(TaskType, verbose_name=_('Monthly expences'), through='MonthlyExpence', limit_choices_to={'active': True})

    # Rajdeep Code
    logged_in = models.BooleanField(_('logged_in'), default=False)
     # End

    def xls_table(self):
        return '<a href="%s">%s</a>' % (reverse('admin:generate_excel', args=[self.id]), ugettext('Download'))
    xls_table.allow_tags = True
    xls_table.short_description = _('Xls table')

    def contacts_table(self):
        return '<a href="%s">%s</a>' % (reverse('admin:generate_contacts', args=[self.id]), ugettext('Download'))
    contacts_table.allow_tags = True
    contacts_table.short_description = _('Contacts table')


    def kasa(self):
        task_types = self.task_set.filter(resolved_by_admin=True, task_type__in=TaskType.objects.filter(can_pay=True)).values_list('task_type_id', flat=True)
        task_types = list(set(task_types))
        tt = self.task_set.filter(task_type_id__in=task_types, resolved_by_admin=True,).aggregate(Sum('price'))
        tt1 = self.task_set.filter(task_type_id__in=task_types, resolved_by_admin=False).aggregate(Sum('partial_paid_total'))
        if not tt['price__sum']:
            tt['price__sum'] = 0

        if not tt1['partial_paid_total__sum']:
            tt1['partial_paid_total__sum'] = 0

        prihod =  tt['price__sum'] + tt1['partial_paid_total__sum']
        # ############################ RAZHODI
        task_types = self.task_set.filter(resolved_by_admin=True, task_type__in=TaskType.objects.filter(can_pay=False)).values_list('task_type_id', flat=True)
        task_types = list(set(task_types))
        tt = self.task_set.filter(task_type_id__in=task_types, resolved_by_admin=True,).aggregate(Sum('price'))
        tt1 = self.task_set.filter(task_type_id__in=task_types, resolved_by_admin=False).aggregate(Sum('partial_paid_total'))
        if not tt['price__sum']:
            tt['price__sum'] = 0

        if not tt1['partial_paid_total__sum']:
            tt1['partial_paid_total__sum'] = 0

        razhod =  tt['price__sum'] + tt1['partial_paid_total__sum']
        return prihod - razhod
    kasa.short_description = _('kasa')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Entrance, self).save(*args, **kwargs)

        _all = Entrance.objects.all()
        pos = 0
        for a in _all:
            pos = pos + 1
            Entrance.objects.filter(id=a.id).update(position=pos)

    class Meta:
        verbose_name = _('Entrance')
        verbose_name_plural = _('Entrances')
        ordering = ('-active', 'title',)


class EntranceDocument(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    document = models.FileField(_('Document'), upload_to='entrancedocuments/%Y/%m')

    entrance = models.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name)

    def file_link(self):
        if self.document:
            return "<a href='%s'>%s</a>" % (self.document.url, self.document.url.rsplit('/', 1)[1])
        else:
            return "-"
    file_link.allow_tags = True
    file_link.short_description = _('File link')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Uploaded document')
        verbose_name_plural = _('Uploaded documents')


class Apartment(models.Model):
    entrance = select2.fields.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name, limit_choices_to={'active': True})
    is_board = models.BooleanField(_('Is Board'), default=False)
    pay_online = models.BooleanField(_('Pay online'), default=False)
    FLOORS = [(i, str(i)) for i in range(-5, 26)]
    OCCUPANTS = [(str(i), str(i)) for i in range(0, 10)]
    floor = models.IntegerField(_('Floor'), max_length=2, choices=FLOORS, default=0)
    apartment = models.CharField(_('Apartment'), max_length=255)
    apartment_integer = models.IntegerField(editable=False, blank=True, null=True)
    common_area = models.DecimalField(_('Common area'), blank=True, null=True, decimal_places=3, max_digits=6)
    monthly_fee = models.DecimalField(_('Monthly fee'), blank=True, null=True, decimal_places=2, max_digits=8)
    contact_person = models.CharField(_('Contact person'), max_length=255, blank=True, null=True)
    contact_phone = models.CharField(_('Contact phone'), max_length=255, blank=True, null=True)
    contact_email = models.CharField(_('Contact email'), max_length=255, blank=True, null=True)
    number_of_occupants = models.CharField(_('Number of occupants'), max_length=2, choices=OCCUPANTS, default=2)
    has_pet = models.BooleanField(_('Has pet'), default=False)
    common_information = RichTextField(_('Common information'), blank=True, null=True)
    client = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to={'is_staff': True})


    def __unicode__(self):
        return "%s.%s | ET. %s, (%s , %s)" % (ugettext('Apartment short'), self.apartment, self.floor, self.contact_person, self.contact_phone)

    def title_short(self):
        return "%s.%s | ET. %s, (%s , %s)" % (ugettext('Apartment short'), self.apartment, self.floor, self.contact_person, self.contact_phone)

    def detach_client(self):
        return '<a href="%s">%s</a>' % (reverse('admin:detach_client', args=[self.id]), ugettext('Detach client'))
    detach_client.allow_tags = True
    detach_client.short_description = _('Detach client')


    def easypay_id(self):
        return "101%s" % self.id
    easypay_id.allow_tags = True
    easypay_id.short_description = _('Easypay Id')

    def get_hash(self, s):
        import hashlib
        m = hashlib.md5()
        m.update(str(s) + settings.SECRET_KEY)
        return str(m.hexdigest())

    def url_for_clients(self):
        if self.client:
            link = 'http://clients.vhodove.bg/auto_login/%s?secret=%s' %(self.client_id, self.get_hash('%s%s' % (self.client.id, self.client.last_login)))
            return '<a href="%s" target="_blank">Link</a>' %link
        else:
            return None
    url_for_clients.allow_tags = True
    url_for_clients.short_description = _('Autologin')

    def save(self, *args, **kwargs):
        try:
            self.apartment_integer = int(re.sub(r"\D", "", self.apartment))
        except:
            self.apartment_integer = 0
        super(Apartment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')
        ordering = ('floor', 'apartment_integer')


class ApartmentDocument(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    document = models.FileField(_('document'), upload_to='apartmentdocuments/%Y/%m')

    apartment = models.ForeignKey(Apartment, verbose_name=Apartment._meta.verbose_name)

    def file_link(self):
        if self.document:
            return "<a href='%s'>%s</a>" % (self.document.url, self.document.url.rsplit('/', 1)[1])
        else:
            return "-"
    file_link.allow_tags = True
    file_link.short_description = _('File link')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Uploaded document')
        verbose_name_plural = _('Uploaded documents')


class MonthlyExpence(models.Model):
    entrance = models.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name)
    task_type = models.ForeignKey(TaskType, verbose_name=TaskType._meta.verbose_name, limit_choices_to={'active': True})
    assignee = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True, limit_choices_to={'is_staff': True})
    price = models.DecimalField(_('Price'), blank=True, null=True, decimal_places=2, max_digits=8)

    def __unicode__(self):
        return self.task_type.title

    class Meta:
        verbose_name = _('Monthly expence')
        verbose_name_plural = _('Monthly expences')


class Income(models.Model):
    class Meta:
        verbose_name = _('Income')
        verbose_name_plural = _('Income')


class EntranceKasa(models.Model):
    class Meta:
        verbose_name = _('EntranceKasa')
        verbose_name_plural = _('EntranceKasa')

class EntranceKasaSummary(models.Model):
    class Meta:
        verbose_name = _('EntranceKasaSummary')
        verbose_name_plural = _('EntranceKasaSummary')


class ZipEntrance(models.Model):
    class Meta:
        verbose_name = _('ZipEntrances')
        verbose_name_plural = _('ZipEntrance')


class PaymentsCashier(models.Model):
    class Meta:
        verbose_name = _('Payments cashier')
        verbose_name_plural = _('Payments cashier')
