# In apps.py, using post_migrate signal
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apscheduler.schedulers.background import BackgroundScheduler
from .scheduler import release_expired_reservations

class CruiseManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cruise_management'

    def ready(self):
        # Connect the post_migrate signal to the scheduler startup
        post_migrate.connect(self.start_scheduler, sender=self)

    def start_scheduler(self, sender, **kwargs):
        # Initialize and start the scheduler only after the app is fully initialized
        scheduler = BackgroundScheduler()
        scheduler.add_job(release_expired_reservations, 'interval', minutes=5)
        scheduler.start()
