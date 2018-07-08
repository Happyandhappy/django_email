from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
import select2.fields

# Mark Django app names for translations
_('Authentication and Authorization')
_('Administration')
_('Please correct the errors below.')
_('Please correct the error below.')


class Document(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    document = models.FileField(_('Document'), upload_to='documents')
    visible_to_groups = select2.fields.ManyToManyField(Group, verbose_name=_('Visible to groups'))
    editable_by_users = models.ManyToManyField(User, verbose_name=_('Editable by users'), limit_choices_to={'is_staff': True})

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
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
