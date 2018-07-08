from django.contrib import admin
from dynamic_costs.models import DynamicCost, ApartmentDynamicCost
from entrances.models import Apartment, Entrance
from tasks.models import Task
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

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


class ApartmentAdminForm(forms.ModelForm):
    class Meta:
        model = Apartment
        exclude = []


class ApartmentInlines(admin.TabularInline):
    model = ApartmentDynamicCost
    extra = 0
    form = ApartmentAdminForm
    fields = ['price', 'is_paid']
    readonly_fields = ('is_paid',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DynamicCostAdmin(admin.ModelAdmin):
    list_display = ('get_priority', 'title', 'entrance', 'price', 'task_type', 'from_date', 'to_date', 'active')
    list_filter = (EntranceListFilter, 'task_type', 'active')
    search_fields = ('title',)
    list_display_links = ('title',)

    def changelist_view(self, request, extra_context=None):
        if 'entrance__id__exact' in request.GET:
            self.list_display = ('get_priority', 'title', 'price', 'task_type', 'from_date', 'to_date', 'active')
        else:
            self.list_display = ('get_priority', 'title', 'entrance', 'price', 'task_type', 'from_date', 'to_date', 'active')
        return super(DynamicCostAdmin, self).changelist_view(request, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        pk_value = obj._get_pk_val()
        return HttpResponseRedirect('/dynamic_costs/dynamiccost/%s' % pk_value)

    def response_change(self, request, obj, post_url_continue=None):
        if '_tasks' in request.POST:
            for a in obj.apartmentdynamiccost_set.all():
                t = Task()
                t.title = obj.title
                t.task_type = obj.task_type
                t.priority = obj.priority
                t.entrance = obj.entrance
                t.from_date = obj.from_date
                t.to_date = obj.to_date
                t.date = obj.from_date
                t.price = a.price
                t.apartment = a.apartment
                t.apartment_dynamic_cost = a
                t.save()
        return HttpResponseRedirect('/dynamic_costs/dynamiccost/')

    def get_form(self, request, instance=None, **kwargs):
        if instance:
            self.readonly_fields = ['entrance']
            if instance.task_type.can_pay:
                self.inlines = [ApartmentInlines]
        else:
            self.readonly_fields = []
        return super(DynamicCostAdmin, self).get_form(request, instance, **kwargs)

admin.site.register(DynamicCost, DynamicCostAdmin)
