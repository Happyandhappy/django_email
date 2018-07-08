from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DynamicCostConfig(AppConfig):
    name = 'dynamic_costs'
    verbose_name = _("Dynamic costs")
