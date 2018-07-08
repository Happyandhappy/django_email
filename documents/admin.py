from django.contrib import admin
from documents.models import Document
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

# Override User display
from django.contrib.auth.models import User


def user_unicode(self):
    if self.first_name:
        return u'%s %s' % (self.first_name, self.last_name)
    else:
        return self.email

User.__unicode__ = user_unicode

#admin.site.unregister(User)
#admin.site.register(User)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            self.readonly_fields = ()
        else:
            self.readonly_fields = ('title',)
            self.exclude.append('visible_to_groups')
            self.exclude.append('editable_by_users')
            if request.user not in obj.editable_by_users.all():
                self.exclude.append('document')
                self.readonly_fields = ('file_link', 'title')
                
        return super(DocumentAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True):
            return Document.objects.all()
        return Document.objects.filter(Q(visible_to_groups__in=request.user.groups.all()) | Q(editable_by_users__in=[request.user])).distinct()
admin.site.register(Document, DocumentAdmin)


#  Django admin log
from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.models import User

action_names = {
    ADDITION: _('Addition'),
    CHANGE: _('Change'),
    DELETION: _('Deletion'),
}


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)


class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = _('User')
    parameter_name = 'user_id'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(pk__in=LogEntry.objects.values_list('user_id').distinct()))


class AdminFilter(UserFilter):
    """Use this filter to only show current Superusers."""
    title = 'admin'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))


class StaffFilter(UserFilter):
    """Use this filter to only show current Staff members."""
    title = 'staff'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    #readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        #'content_type',
        'object_link',
        #'action_flag',
        #'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return (request.user.is_superuser or 4 in request.user.groups.all().values_list('id', flat=True)) and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = _('object')

    def get_queryset(self, request):
        return super(LogEntryAdmin, self).get_queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)
