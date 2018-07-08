from django.contrib import admin
from nomenclatures.models import TaskType, Priority
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from entrances.models import Apartment, Entrance
from django.db.models import Q


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'can_pay', 'can_pay_partial', 'for_cachiers', 'is_administrative', 'active', 'price_for_resolve')


class PriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'title', 'default', 'active')
    list_editable = ['color']

admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Priority, PriorityAdmin)


from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

class EntranceListFilter(SimpleListFilter):
    title = _('Entrance')
    parameter_name = 'entrance__id__exact'

    def lookups(self, request, model_admin):
        return [(c.id, "%s. %s" %(c.position, c.title)) for c in Entrance.objects.filter(active=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(content_type=10,object_id__in=Task.objects.filter(entrance_id=self.value()).values_list('id', flat=True)) | Q(content_type=13,object_id=self.value()) | Q(content_type=15,object_id__in=Apartment.objects.filter(entrance_id=self.value()).values_list('id', flat=True)))
        else:
            return queryset

class ApartmentsListFilter(SimpleListFilter):
    title = _('Apartment')
    parameter_name = 'apartment'

    def lookups(self, request, model_admin):
        return Apartment.objects.filter(entrance_id=request.GET.get('entrance__id__exact', 0)).values_list('id', 'apartment')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(content_type=15,object_id=self.value()) | Q(content_type=10,object_id__in=Task.objects.filter(apartment_id=self.value()).values_list('id', flat=True)))
        else:
            return queryset


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    list_filter = [
        #'user',
        EntranceListFilter,
        ApartmentsListFilter
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'get_entrance',
        'get_apartment',
        'content_type',
        'object_link',
        'change_message',
    ]


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def get_entrance(self, obj):
        try:
            o = obj.get_edited_object()
            return o if isinstance(o, Entrance) else o.entrance
        except:
            return '-'
    get_entrance.short_description = _("Entrance")

    def get_apartment(self, obj):
        try:
            o = obj.get_edited_object()
            return o if isinstance(o, Apartment) else o.apartment
        except:
            return '-'

    get_apartment.short_description = _("Apartment")

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'


    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request).exclude(content_type_id__in=[1,4]).prefetch_related('content_type', 'user')

admin.site.unregister(LogEntry)
admin.site.register(LogEntry, LogEntryAdmin)
