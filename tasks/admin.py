from django.contrib import admin
from tasks.models import Task, TaskDocument, Schedule, PartialTaskPay, PaymentAhead
from dynamic_costs.models import DynamicCost, ApartmentDynamicCost
from nomenclatures.models import TaskType, Priority
from django.contrib.auth.models import User
from entrances.models import Apartment, Entrance
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime
from django.utils.encoding import force_text
from django.http import HttpResponse
from django.conf.urls import url, patterns
from django.forms.extras.widgets import SelectDateWidget
from django.db import models
from vhodove.helper import first_day_of_month
from django.views.generic import View

from vhodove.utils import render_to_pdf #created in step 4

class ApartmentsListFilter(SimpleListFilter):
    title = _('Apartment')
    parameter_name = 'apartment'

    def lookups(self, request, model_admin):
        return Apartment.objects.filter(entrance_id=request.GET.get('entrance__id__exact', 0)).values_list('id', 'apartment')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(apartment_id=self.value())
        else:
            return queryset

# Rajdeep Code

class TimespanListFilter(SimpleListFilter):
    title = _('Timespan')
    parameter_name = 'timespan'

    def lookups(self, request, model_admin):
        return (
            ('past',_('Till Now')),
            ('future',_('From Now'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'past':
            return queryset.filter(updated_at__lte=datetime.date.today())

        if self.value() == 'future':
            return queryset.filter(updated_at__gte=datetime.date.today())

# End


class FloorListFilter(SimpleListFilter):
    title = _('Floor')
    parameter_name = 'floor'

    def lookups(self, request, model_admin):
        return Apartment.FLOORS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(apartment__floor=self.value())
        else:
            return queryset


class ResolvedListFilter(SimpleListFilter):
    title = _('Resolved')
    parameter_name = 'resolved__exact'

    def lookups(self, request, model_admin):
        return ((2, _('Yes')), (1, _('No')), (-1, _('All')))

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() and self.value() != '-1':
            value = int(self.value()) - 1
            return queryset.filter(resolved=value)
        else:
            return queryset

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

class ResolvedByAdminListFilter(SimpleListFilter):
    title = _('Resolved by admin')
    parameter_name = 'resolved_by_admin__exact'

    def lookups(self, request, model_admin):
        return ((2, _('Yes')), (1, _('No')), (-1, _('All')))

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() and self.value() != '-1':
            value = int(self.value()) - 1
            return queryset.filter(resolved_by_admin=value)
        else:
            return queryset

class HasEasyPayListFilter(SimpleListFilter):
    title = _('Easypay code')
    parameter_name = 'easypay'

    def lookups(self, request, model_admin):
        return ((2, _('Yes')), (1, _('No')), (-1, _('All')))

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() and self.value() != '-1':
            value = int(self.value())
            if value == 2:
                return queryset.filter(easypay_code__isnull=False)
            else:
                return queryset.filter(easypay_code__isnull=True)

        else:
            return queryset


class TaskDocumentInlines(admin.TabularInline):
    model = TaskDocument
    extra = 0


class PartialTaskPayInlines(admin.TabularInline):
    model = PartialTaskPay
    extra = 0

    readonly_fields = ['assignee', 'created_at']

#Rajdeep Code Start
class PartialTaskPayAdmin(admin.ModelAdmin):
    from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
    search_fields = ('assignee__username','assignee__first_name','assignee__last_name')
    list_display = ('assignee','task','created_at','price','easypay_code')
    list_filter = (
            ('created_at', DateRangeFilter),
            # ('created_at', DateTimeRangeFilter),
        )
#End


class PaymentAheadAdmin(admin.ModelAdmin):
    list_display = ('entrance', 'apartment', 'assignee', 'from_date', 'period')
    list_filter = (EntranceListFilter, ApartmentsListFilter, 'assignee')
    list_display_links = None
    #readonly_fields = ['from_date',]

    def get_form(self, request, obj=None, **kwargs):
        y = datetime.date.today().year
        m = datetime.date.today().month + 1
        if m == 13:
            m = 1
            y = y+1
        form = super(PaymentAheadAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['from_date'].initial = first_day_of_month(datetime.date(y, m, 1))
        return form


    def get_apartment_payment_fee(self, request):
        try:
            o = Apartment.objects.get(pk=request.GET.get('apartment_id'))
            return HttpResponse(o.monthly_fee)
        except:
            return HttpResponse(0)

    def get_urls(self):
        urls = super(PaymentAheadAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'^get_apartment_payment_fee/$',
                self.admin_site.admin_view(self.get_apartment_payment_fee)
            ),
        )
        return my_urls + urls


    def has_change_permission(self, request, obj=None):
        return obj is None

    def has_delete_permission1(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.assignee = request.user
        obj.save()


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('title', 'entrance__title', 'apartment__apartment')
    list_display = ('id', 'title', 'entrance', 'apartment')
    list_display_links = ('title', 'entrance', 'apartment')
    # list_filter = (TimespanListFilter,)
    list_per_page = 50
    actions = ['mark_as_resolved_by_admin', 'mark_as_resolved', 'unmark_as_resolved_by_admin', 'unmark_as_resolved']

    def mark_as_resolved_by_admin(self, request, queryset):
        queryset.update(resolved_by_admin=True)
    mark_as_resolved_by_admin.short_description = _("Mark as resolved by admin")

    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved=True)
    mark_as_resolved.short_description = _("Mark as resolved")

    def unmark_as_resolved_by_admin(self, request, queryset):
        queryset.update(resolved_by_admin=False)
    unmark_as_resolved_by_admin.short_description = _("Unmark as resolved by admin")

    def unmark_as_resolved(self, request, queryset):
        queryset.update(resolved=False)
    unmark_as_resolved.short_description = _("Unmark as resolved")


    formfield_overrides = {
        models.DateField: {'widget': SelectDateWidget(years=('2015','2016','2017','2018','2019','2020'))},
    }

    def get_actions(self, request):
        actions = super(TaskAdmin, self).get_actions(request)
        if 'delete_selected' in actions and not request.user.is_superuser:
                del actions['delete_selected']

        if not request.user.is_superuser:
            del actions['mark_as_resolved_by_admin']
            del actions['mark_as_resolved']
            del actions['unmark_as_resolved_by_admin']
            del actions['unmark_as_resolved']
        return actions

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(TaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'task_type':
            if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
                field.queryset = field.queryset.all()
            else:
                field.queryset = field.queryset.filter(for_cachiers=True)

        if db_field.name == 'entrance':
            if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
                field.queryset = field.queryset.all()
            else:
                entrance_ids = Schedule.objects.filter(assignee=request.user, from_date__lte=datetime.datetime.now, to_date__gte=datetime.datetime.now).values_list('entrance_id')
                qs = qs.filter(Q(assignee=request.user) | Q(assignee__isnull=True, entrance_id__in=entrance_ids))
                # field.queryset = field.queryset.filter(id__in=entrance_ids)

        return field

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, PartialTaskPay):  #Check if it is the correct type of inline
                if not instance.assignee_id:
                    instance.assignee = request.user
                instance.save()
        super(TaskAdmin, self).save_formset(request, form, formset, change)

    def changelist_view(self, request, extra_context=None):
        self.assignees_list = {x['id']:x for x in User.objects.filter(is_staff=True).values('id','first_name','last_name')}
        self.priorities_list = dict(Priority.objects.all().values_list('id','color'))
        self.task_types_list = dict(TaskType.objects.all().values_list('id','title'))
        self.apartments_list = {x['id']:x for x in Apartment.objects.filter(id__in=self.get_queryset(request).values_list('apartment_id', flat=True)).values('id','floor','contact_person','contact_phone', 'contact_email', 'pay_online', 'apartment', 'number_of_occupants')}
        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            # self.list_filter = (ResolvedListFilter, ResolvedByAdminListFilter, HasEasyPayListFilter, EntranceListFilter, ApartmentsListFilter, FloorListFilter, 'assignee', 'task_type', 'priority')

            # Rajdeep Code Start
            self.list_filter = (TimespanListFilter,ResolvedListFilter, ResolvedByAdminListFilter, HasEasyPayListFilter, EntranceListFilter, ApartmentsListFilter, FloorListFilter, 'assignee', 'task_type', 'priority')

            # End
            self.list_editable = ('document',)
            if 'entrance__id__exact' in request.GET:
                if request.GET.get('resolved_by_admin__exact',0) == '2':
                    self.list_per_page = 50
                else:
                    self.list_per_page = 50000
                self.list_display = ('get_priority', 'title', 'get_apartment', 'get_floor', 'get_contact_info', 'get_occupants','price', 'partial_paid_total', 'get_date', 'get_assignee', 'normalized_time', 'get_task_type','resolved', 'resolved_by_admin')
            else:
                self.list_per_page = 50
                self.list_display = ('get_priority', 'title', 'entrance', 'get_apartment', 'get_floor', 'get_contact_info', 'get_occupants', 'price', 'partial_paid_total', 'get_date', 'get_assignee', 'normalized_time', 'get_task_type','resolved', 'resolved_by_admin')

            if not request.GET.has_key('resolved__exact'):
                q = request.GET.copy()
                q['resolved__exact'] = '1'
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()

            if not request.GET.has_key('resolved_by_admin__exact'):
                q = request.GET.copy()
                q['resolved_by_admin__exact'] = '1'
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()
        else:
            # self.list_filter = (ResolvedListFilter, EntranceListFilter, ApartmentsListFilter, FloorListFilter) #old

            # Rajdeep Code Start
            if request.user.is_staff:
                self.list_filter = (ResolvedListFilter, EntranceListFilter, ApartmentsListFilter, FloorListFilter)
            else:
                self.list_filter = (ResolvedListFilter, ApartmentsListFilter, FloorListFilter)
            # End
            self.list_editable = ('document',)
            if 'entrance__id__exact' in request.GET:
                self.list_display = ('get_priority', 'title', 'get_apartment', 'get_floor', 'get_contact_info','get_occupants', 'price', 'partial_paid_total', 'date', 'get_task_type','resolved')
            else:
                self.list_display = ('get_priority', 'title', 'entrance', 'get_apartment', 'get_floor', 'get_contact_info', 'get_occupants', 'price', 'partial_paid_total', 'date', 'get_task_type','resolved')


            if not request.GET.has_key('resolved__exact'):
                q = request.GET.copy()
                q['resolved__exact'] = '1'
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()

        extra_context = extra_context or {}
        from django.db.models import Sum
        ChangeList = self.get_changelist(request)
        cl = ChangeList(request, self.model, self.list_display, self.list_display_links, self.list_filter, self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page, self.list_max_show_all, self.list_editable, self)
        qs = cl.get_queryset(request)
        sum_price = qs.aggregate(Sum('price'))['price__sum']
        sum_partial =qs.aggregate(Sum('partial_paid_total'))['partial_paid_total__sum']
        sum_price = sum_price if sum_price else 0
        sum_partial = sum_partial if sum_partial else 0
        extra_context['total'] = sum_price - sum_partial
        extra_context['has_entrance_filter'] = 'entrance__id__exact' in request.GET and self.list_per_page > 50
        return super(TaskAdmin, self).changelist_view(request, extra_context)

    def get_contact_info(self, obj):
        if obj.apartment_id:
            return '<a href="%s">Easypay: 101%s<br />%s<br />%s<br />%s<br /></a><span style="font-weight:bold;color:#dd0000;">%s</span>' % (reverse('admin:entrances_apartment_change', args=[obj.apartment_id]), obj.apartment_id, self.apartments_list[obj.apartment_id]['contact_person'], self.apartments_list[obj.apartment_id]['contact_phone'] or '-', self.apartments_list[obj.apartment_id]['contact_email'] or '-', _('Pay online') if self.apartments_list[obj.apartment_id]['pay_online'] else '')
        else:
            return None
    get_contact_info.short_description = _('Get Contact info')
    get_contact_info.allow_tags = True

    def get_priority(self, obj):
        return '<span style="background:%s;display:block;width:22px;height:22px;"></span>' % (self.priorities_list[obj.priority_id])

    get_priority.short_description = ''
    get_priority.allow_tags = True

    def normalized_time(self, obj):
        return obj.updated_at.strftime("%d.%m.%Y")
    normalized_time.short_description = _('Updated at')

    def get_apartment(self, obj):
        if obj.apartment_id:
            return self.apartments_list[obj.apartment_id]['apartment']
        else:
            return None
    get_apartment.short_description = _('Apartment')
    get_apartment.admin_order_field = 'apartment__apartment_integer'

    def get_floor(self, obj):
        if obj.apartment_id:
            return self.apartments_list[obj.apartment_id]['floor']
        else:
            return None
    get_floor.admin_order_field = 'apartment__floor'
    get_floor.short_description = _('Floor')


    def get_task_type(self, obj):
        return self.task_types_list[obj.task_type_id]
    get_task_type.short_description = _('Task type')

    def get_assignee(self, obj):
        if obj.assignee_id and obj.assignee_id in self.assignees_list:
            return "%s %s" %(self.assignees_list[obj.assignee_id]['first_name'], self.assignees_list[obj.assignee_id]['last_name'])
        else:
            return ''
    get_assignee.short_description = _('User')




    def get_occupants(self, obj):
        if obj.apartment_id:
            return self.apartments_list[obj.apartment_id]['number_of_occupants']
        else:
            return None
    get_occupants.admin_order_field = 'apartment__number_of_occupants'
    get_occupants.short_description = _('Number of occupants')

    def readonly_clickable_document(self, instance):
        return '<a href="%s" target="_blank">%s</a>' %(instance.document.url,instance.document)

    readonly_clickable_document.short_description = _('Document')
    readonly_clickable_document.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.resolved_by_admin and not request.user.is_superuser:
            return list(set(
                [field.name if field.editable and field.name not in ['document', 'can_pay_partial', 'can_pay', 'price_for_resolve'] else 'id' for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many] +
                ['readonly_clickable_document']
            ))

        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = []
        self.exclude = ['templates', 'can_pay', 'can_pay_partial']
        if obj and obj.resolved_by_admin and not request.user.is_superuser:
            self.exclude.append('document')
        if obj:
            self.readonly_fields = ['task_type', 'apartment', 'entrance', 'easypay_code']

            #if not obj.task_type.can_pay:
            #    self.exclude.append('price')

            if not obj.task_type.can_pay_partial:
                #self.exclude.append('partial_paid')
                self.inlines = [TaskDocumentInlines]
            else:
                self.inlines = [PartialTaskPayInlines, TaskDocumentInlines]

        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            self.exclude.append('resolved_by_admin')
            self.exclude.append('assignee')
            self.exclude.append('apartment')
            if obj is not None and obj.task_type.can_pay_partial:
                self.readonly_fields.append('resolved')
                self.readonly_fields.append('partial_paid_total')
                self.readonly_fields.append('price')

            if 2 not in request.user.groups.all().values_list('id', flat=True) and obj is not None:
                self.readonly_fields.append('priority')
                self.readonly_fields.append('title')


        return super(TaskAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            obj.assignee = request.user

        if obj.resolved and not obj.assignee and not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            obj.assignee = request.user

        obj.save()

    def get_queryset(self, request):
        qs = super(TaskAdmin, self).get_queryset(request)
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            entrance_ids = Schedule.objects.filter(assignee=request.user, from_date__lte=datetime.datetime.now, to_date__gte=datetime.datetime.now).values_list('entrance_id')
            qs = qs.filter(Q(assignee=request.user) | Q(assignee__isnull=True, entrance_id__in=entrance_ids) | Q(updated_at__gte=datetime.date.today()))
        qs = qs.filter(Q(updated_at__lte=datetime.date.today()))
        return qs

class GeneratePDF(View, models.Model):
     def get(self, request, *args, **kwargs):
         template = get_template('invoice.html')
         entrance = select2.fields.ForeignKey(Entrance, verbose_name=Entrance._meta.verbose_name, blank=True, null=True, limit_choices_to={'active': True})
         assignee = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True, limit_choices_to={'is_staff': True})
         from_date = models.DateField(_('From date'), default=first_day_of_month)
         to_date = models.DateField(_('To date'), default=last_day_of_month)
         visit_date = models.DateField(_('Visit date'), default=datetime.date.today)
         period = models.IntegerField(_('Period'))
         price = models.DecimalField(_('Price'), blank=True, null=True, decimal_places=2, max_digits=8)
         partial_paid = models.DecimalField(_('Partial paid'), blank=True, null=True, decimal_places=2, max_digits=8, editable=False)
         context = {
             "for_apartment": Apartment,
             "for_entrance": entrance,
             "partial_paid": partial_paid,
             "period": period,
             "amount": price,
             "cashier": assignee,
             "today": visit_date,
         }
         html = template.render(context)
         pdf = render_to_pdf('invoice.html', context)
         if pdf:
             response = HttpResponse(pdf, content_type='application/pdf')
             filename = "Invoice_%s.pdf" %("12341231")
             content = "inline; filename='%s'" %(filename)
             download = request.GET.get("download")
             if download:
                 content = "attachment; filename='%s'" %(filename)
             response['Content-Disposition'] = content
             return response
         return HttpResponse("Not found")


class ScheduleAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            self.list_editable = ('assignee', 'from_date', 'to_date', 'visit_date')
            self.list_filter = ['assignee', EntranceListFilter]
            if 'entrance__id__exact' in request.GET:
                self.list_display = ('id','assignee', 'from_date', 'to_date', 'visit_date')
            else:
                self.list_display = ('entrance', 'assignee', 'from_date', 'to_date', 'visit_date')

        else:
            self.list_display = ('entrance', 'assignee', 'visit_date')
            self.list_editable = []
            self.list_filter = []

        return super(ScheduleAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(ScheduleAdmin, self).get_queryset(request)
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            if 2 not in request.user.groups.all().values_list('id', flat=True):
                qs = qs.filter(assignee=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ()
        self.exclude = []
        if not request.user.is_superuser and 4 not in request.user.groups.all().values_list('id', flat=True):
            self.readonly_fields = ('entrance', 'visit_date')
            self.exclude.append('from_date')
            self.exclude.append('to_date')
            self.exclude.append('assignee')

        return super(ScheduleAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(PartialTaskPay,PartialTaskPayAdmin) #Rajdeep

admin.site.register(Task, TaskAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(PaymentAhead, PaymentAheadAdmin)
