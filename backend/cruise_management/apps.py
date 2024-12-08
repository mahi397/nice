import logging
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from apscheduler.schedulers.background import BackgroundScheduler
from .scheduler import release_expired_trip_reservations, release_expired_room_reservations

logger = logging.getLogger(__name__)

class CruiseManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cruise_management'

    def ready(self):
        """
        Connects the post_migrate signal to start the scheduler.
        """
        logger.info("CruiseManagementConfig is ready. Connecting to post_migrate signal.")
        post_migrate.connect(self.start_scheduler, sender=self)

    def start_scheduler(self, *args, **kwargs):
        """
        Starts the scheduler to release expired reservations every minute.
        This method is connected to the `post_migrate` signal.
        """
        logger.info("Post-migrate signal triggered. Starting scheduler...")
        scheduler = BackgroundScheduler()

        # Add jobs to release expired trip and room reservations
        try:
            scheduler.add_job(release_expired_trip_reservations, 'interval', minutes=1)
            scheduler.add_job(release_expired_room_reservations, 'interval', minutes=1)

            # Check if jobs are added
            logger.info(f"Jobs added: {scheduler.get_jobs()}")

            # Start the scheduler only once
            scheduler.start()
            logger.info("Scheduler started successfully.")
            logger.info(f"Scheduler running: {scheduler._thread.is_alive()}")

        except Exception as e:
            logger.error(f"Error starting the scheduler: {e}", exc_info=True)
