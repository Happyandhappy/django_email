from django.contrib import admin
from django import forms
from entrances.models import Entrance, Apartment, MonthlyExpence, Income, EntranceDocument, ApartmentDocument, PaymentsCashier, ZipEntrance, EntranceKasa, EntranceKasaSummary
from nomenclatures.models import TaskType, Priority
from django.http import HttpResponseRedirect
from tasks.models import Task, Schedule
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
import datetime
from vhodove.helper import first_day_of_month, last_day_of_month
from django.contrib.admin import widgets
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from entrances.helper import EntranceToXls, IncomeToXls, CashierIncomeToXls
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import PermissionDenied

class EntranceListFilter(SimpleListFilter):
    title = _('Entrance')
    parameter_name = 'entrance__id__exact'

    def lookups(self, request, model_admin):
        return [(c.id, "%s. %s" %(c.position, c.title)) for c in Entrance.objects.filter(active=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(entrance__id__exact=self.value())
        else:
            return queryset

class ApartmentsNumberFilter(SimpleListFilter):
    title = _('Apartment')
    parameter_name = 'apartment'

    def lookups(self, request, model_admin):
        return Apartment.objects.filter(entrance_id=request.GET.get('entrance__id__exact', 0)).values_list('id', 'apartment')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
        else:
            return queryset


class EntranceDocumentInlines(admin.TabularInline):
    model = EntranceDocument
    extra = 0

    def get_fields(self, request, obj=None):
        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            form = self.get_formset(request, obj, fields=None).form
            return list(form.base_fields) + list(self.get_readonly_fields(request, obj))
        else:
            return ('title', 'file_link')

    def get_readonly_fields(self, request, obj=None):
        fields = []
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            fields.append('title')
            # fields.append('document')
            fields.append('file_link')
        return fields


class ApartmentDocumentInlines(admin.TabularInline):
    model = ApartmentDocument
    extra = 0


class MonthlyExpenceForm(forms.ModelForm):
    class Meta:
        model = TaskType
        exclude = []


class MonthlyExpenceInlines(admin.TabularInline):
    model = MonthlyExpence
    extra = 0
    form = MonthlyExpenceForm


class ApartmentInlines(admin.TabularInline):
    model = Apartment
    extra = 0
    exclude = ['common_information']

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class EntranceAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'active', 'auto_assign_monthly_tasks')
    list_display_links = ['title']
    inlines = [MonthlyExpenceInlines, ApartmentInlines, EntranceDocumentInlines]

    # Rajdeep Code Start
    actions = ['change_status_true','change_status_false']

    def change_status_true(self, request, queryset):
        queryset.update(logged_in=True)
    change_status_true.short_description = _("Mark as Logged In")

    def change_status_false(self, request, queryset):
        queryset.update(logged_in=False)
    change_status_false.short_description = _("Unmark as Logged In")

    # End

    def changelist_view(self, request, extra_context=None):

        self.customs_list = MonthlyExpence.objects.filter(task_type_id__in=[2,6,7,64]).values('entrance_id','task_type_id','price')

        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True) or 2 in request.user.groups.all().values_list('id', flat=True):
            self.list_display = ('logged_in','position', 'title', 'active', 'auto_assign_monthly_tasks','custom_2','custom_64', 'custom_7','custom_6', 'kasa','xls_table', 'contacts_table')
        else:
            self.list_display = ('position', 'title', 'active', 'auto_assign_monthly_tasks')

        return super(EntranceAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(EntranceAdmin, self).get_queryset(request)
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            qs = qs.filter(id__in=Schedule.objects.filter(assignee=request.user, from_date__lte=datetime.datetime.now, to_date__gte=datetime.datetime.now).values_list('entrance_id', flat=True))
        return qs

    def tax_form_safe(self, instance):
        return mark_safe(instance.tax_form)
    tax_form_safe.short_description = _('Tax form')
    tax_form_safe.allow_tags = True

    def common_information_safe(self, instance):
        return mark_safe(instance.common_information)
    common_information_safe.short_description = _('Common information')
    common_information_safe.allow_tags = True

    def google_maps_safe(self, instance):
        return '<a href="%s" target="_blank">%s</a>' % (instance.google_maps, instance.google_maps)
    google_maps_safe.short_description = _('Google maps')
    google_maps_safe.allow_tags = True


    def custom_2(self, obj):
        for m in self.customs_list:
            if m['entrance_id'] == obj.id and m['task_type_id'] == 2:
                return m['price']
        return '-'
    custom_2.short_description = _('taksa_domoupravitel')

    def custom_64(self, obj):
        for m in self.customs_list:
            if m['entrance_id'] == obj.id and m['task_type_id'] == 64:
                return m['price']
        return '-'
    custom_64.short_description = _('taksa_kasierstvo')

    def custom_7(self, obj):
        for m in self.customs_list:
            if m['entrance_id'] == obj.id and m['task_type_id'] == 7:
                return m['price']
        return '-'
    custom_7.short_description = _('abonamentno_pochistvane')

    def custom_6(self,obj):
        for m in self.customs_list:
            if m['entrance_id'] == obj.id and m['task_type_id'] == 6:
                return m['price']
        return '-'
    custom_6.short_description = _('poddrujka_asansior')

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = []
        self.exclude = []
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            self.exclude.append('active')
            self.exclude.append('tax_amount')
            self.exclude.append('tax_form')
            self.exclude.append('common_information')
            self.exclude.append('google_maps')

            self.readonly_fields.append('title')
            self.readonly_fields.append('google_maps_safe')
            self.readonly_fields.append('tax_form_safe')
            self.readonly_fields.append('contract_date')
            self.readonly_fields.append('protocol_date')
            self.readonly_fields.append('common_information_safe')

        return super(EntranceAdmin, self).get_form(request, obj, **kwargs)

    def get_urls(self):
        urls = super(EntranceAdmin, self).get_urls()
        my_urls = patterns('', url(r'^(?P<id>[-\d]+)/generate_tasks/$', self.admin_site.admin_view(self.generate_tasks), name='generate_tasks'),)
        my_urls += patterns('', url(r'^(?P<id>[-\d]+)/generate_excel/$', self.admin_site.admin_view(self.generate_excel), name='generate_excel'),)
        my_urls += patterns('', url(r'^(?P<id>[-\d]+)/generate_contacts/$', self.admin_site.admin_view(self.generate_contacts), name='generate_contacts'),)
        my_urls += patterns('', url(r'^(?P<id>[-\d]+)/generate_static/$', self.admin_site.admin_view(self.generate_static), name='generate_static'),)

        return my_urls + urls


    class TasksForm(forms.Form):
        from_date = forms.DateField(initial=first_day_of_month, required=True, widget=widgets.AdminDateWidget)
        to_date = forms.DateField(initial=last_day_of_month, required=True, widget=widgets.AdminDateWidget)

    def generate_excel(self, request, id):

        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        import os

        ee = EntranceToXls(id)
        filename = ee.create_xls()
        response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)


        return response

    def generate_contacts(self, request, id):

        ee = EntranceToXls(id)
        filename = ee.create_contacts_xls()

        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        import os
        response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
        return response

    def generate_static(self, request, id):

        ee = EntranceToXls(id)
        filename = ee.create_static_xls()

        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        import os
        response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
        return response

    @csrf_exempt
    def generate_tasks(self, request, id):
        opts = Entrance._meta
        app_label = opts.app_label
        form = None
        obj = Entrance.objects.get(pk=id)

        monthly_expences = MonthlyExpence.objects.filter(entrance=obj)
        apartments = Apartment.objects.filter(entrance=obj)

        if '_save' in request.POST:
            f = request.POST.get('from_date').split('.')
            to = request.POST.get('to_date').split('.')
            for m in monthly_expences:
                t = Task()
                t.title = m.task_type.title
                t.task_type = m.task_type
                t.priority = Priority.objects.get(default=True)
                t.entrance = obj
                t.from_date = datetime.date(int(f[2]), int(f[1]), int(f[0]))
                t.to_date = datetime.date(int(to[2]), int(to[1]), int(to[0]))
                t.date = datetime.date(int(f[2]), int(f[1]), int(f[0]))
                t.assignee = m.assignee
                t.price = request.POST.get('monthly_expences.%s' % m.id) if request.POST.get('monthly_expences.%s' % m.id) else 0
                t.save()

            task_type_fee = TaskType.objects.get(default_fee=True)

            for a in apartments:
                if not Task.objects.filter(task_type=task_type_fee, entrance=obj, apartment=a, from_date=datetime.date(int(f[2]), int(f[1]), int(f[0])), to_date=datetime.date(int(to[2]), int(to[1]), int(to[0]))).exists():
                    t = Task()
                    t.title = task_type_fee.__unicode__()
                    t.task_type = task_type_fee
                    t.priority = Priority.objects.get(default=True)
                    t.entrance = obj
                    t.apartment = a
                    t.from_date = datetime.date(int(f[2]), int(f[1]), int(f[0]))
                    t.to_date = datetime.date(int(to[2]), int(to[1]), int(to[0]))
                    t.date = datetime.date(int(f[2]), int(f[1]), int(f[0]))
                    t.price = request.POST.get('apartments.%s' % a.id) if request.POST.get('apartments.%s' % a.id) else 0
                    t.save()

            return HttpResponseRedirect(reverse('admin:tasks_task_changelist'))

        if not form:
            form = self.TasksForm()

        return render_to_response('entrances/admin_generate_tasks_change_form.html', {"form": form, "opts": opts, "app_label": app_label, 'monthly_expences': monthly_expences, 'apartments': apartments})


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['entrance', 'floor', 'apartment', 'contact_person', 'contact_email', 'contact_phone', 'monthly_fee', 'number_of_occupants', 'common_area','is_board' , 'easypay_id']
    list_display_links = ['entrance', 'floor', 'apartment', 'contact_person', 'number_of_occupants']
    list_filter = (EntranceListFilter, ApartmentsNumberFilter, 'floor', 'is_board')
    search_fields = ('contact_person', 'contact_email', 'contact_phone')

    inlines = [ApartmentDocumentInlines]

    def changelist_view(self, request, extra_context=None):
        if 'entrance__id__exact' in request.GET:
            self.list_display = ['floor', 'apartment', 'contact_person', 'contact_email', 'contact_phone', 'monthly_fee', 'number_of_occupants', 'common_area', 'is_board', 'pay_online', 'easypay_id']
            self.list_display_links = ['floor', 'apartment', 'contact_person', 'number_of_occupants']
        else:
            self.list_display = ['entrance', 'floor', 'apartment', 'contact_person', 'contact_email', 'contact_phone', 'monthly_fee','number_of_occupants', 'common_area', 'is_board', 'pay_online', 'easypay_id']
            self.list_display_links = ['entrance', 'floor', 'apartment', 'contact_person', 'number_of_occupants']

        if request.user.is_superuser:
            self.list_display.append('detach_client')

        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            self.list_display.append('url_for_clients')

        return super(ApartmentAdmin, self).changelist_view(request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ['client']
        self.exclude = []
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):  # TODO - TOVA VAJI SAMO ZA "KASIERITE"
            self.readonly_fields.append('entrance')
            self.readonly_fields.append('floor')
            self.readonly_fields.append('apartment')
            self.readonly_fields.append('common_area')
            self.readonly_fields.append('monthly_fee')
            self.readonly_fields.append('number_of_occupants')
            self.readonly_fields.append('common_information')

        return super(ApartmentAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(ApartmentAdmin, self).get_queryset(request)
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            qs = qs.filter(entrance_id__in=Schedule.objects.filter(assignee=request.user, from_date__lte=datetime.datetime.now, to_date__gte=datetime.datetime.now).values_list('entrance_id', flat=True))
        return qs

    def get_urls(self):
        urls = super(ApartmentAdmin, self).get_urls()
        my_urls = patterns('', url(r'^(?P<id>[-\d]+)/detach_client/$', self.admin_site.admin_view(self.detach_client_function), name='detach_client'),)
        return my_urls + urls

    def detach_client_function(self, request, id):

        a = Apartment.objects.get(pk=id)
        a.client = None
        a.contact_email = "%s [!]" % a.contact_email
        a.save()

        if 'return' in request.GET:
            return HttpResponseRedirect(request.GET.get('return'))
        return HttpResponseRedirect('/entrances/apartment/')

admin.site.register(Entrance, EntranceAdmin)
admin.site.register(Apartment, ApartmentAdmin)


class IncomeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if request.user.is_staff: # Rajdeep Code
            ee = IncomeToXls()
            filename = ee.create_xls()

            from django.http import HttpResponse
            from django.core.servers.basehttp import FileWrapper
            import os
            response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
            return response
        raise PermissionDenied

admin.site.register(Income, IncomeAdmin)

class EntranceKasaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        ee = IncomeToXls()
        filename = ee.create_kasa_xls()

        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        import os
        response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
        return response

#admin.site.register(EntranceKasa, EntranceKasaAdmin)

class ZipEntranceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponse
        import zipfile
        import StringIO
        import os

        _all = Entrance.objects.filter(active=1)
        filenames = []
        for a in _all:
            ee = EntranceToXls(a.id)
            filenames.append(ee.create_xls())
        filename = "Vhodove.zip"
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")
        for fpath in filenames:
            zf.write(fpath, os.path.basename(fpath))
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)


        return response

admin.site.register(ZipEntrance, ZipEntranceAdmin)


class EntranceKasaSummaryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        ee = IncomeToXls()
        filename = ee.create_kasa_xls_summary()

        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        import os
        response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
        return response

admin.site.register(EntranceKasaSummary, EntranceKasaSummaryAdmin)

class PaymentsCashiersAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        ee = CashierIncomeToXls()
        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            filename = ee.create_xls()
        else:
            filename = ee.create_xls(user_id=request.user.id)

        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        import os
        response = HttpResponse(FileWrapper(file(filename)), content_type='application/excell')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
        return response

admin.site.register(PaymentsCashier, PaymentsCashiersAdmin)
