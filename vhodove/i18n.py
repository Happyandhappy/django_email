'''
Fake file to translate messages from django.contrib.auth.
'''
from django.utils.translation import ugettext_lazy as _


def fake():
    _('Please correct the errors below.')
    _('Please correct the error below.')
