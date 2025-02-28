from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.crm'

    def ready(self):
        logger.info("Initializing CRM app signals")
        import apps.crm.signals

