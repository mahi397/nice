from django.apps import AppConfig


class CruiseManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cruise_management'
    
    #def ready(self):
        #import cruise_management.signals  # Ensure signals are loaded
