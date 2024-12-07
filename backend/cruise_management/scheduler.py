from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta


def release_expired_reservations():
    from .models import MmsTrip
    expiration_time = timedelta(minutes=5)
    now = timezone.now()

    expired_trips = MmsTrip.objects.filter(
        tempcapacityreserved=True,
        tempreservationtimestamp__lte=now - expiration_time
    )

    for trip in expired_trips:
        trip.tripcapacityremaining += trip.tempcapacitynumber
        trip.tempreservationtimestamp = None
        trip.tempcapacitynumber = 0
        trip.save()

    print(f"Released {len(expired_trips)} expired temporary reservations.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(release_expired_reservations, 'interval', minutes=5)
    scheduler.start()