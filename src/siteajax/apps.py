from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SiteajaxConfig(AppConfig):
    """Application configuration."""

    name = 'siteajax'
    verbose_name = _('Siteajax')
