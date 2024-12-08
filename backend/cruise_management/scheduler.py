from datetime import timedelta
from django.utils import timezone
import logging

# Set up logger
logger = logging.getLogger(__name__)

def release_expired_trip_reservations():
    """
    Releases expired temporary trip reservations (capacity) that were not finalized.
    """
    from .models import MmsTrip
    expiration_time = timedelta(minutes=5)
    now = timezone.now()

    try:
        expired_trips = MmsTrip.objects.filter(
            tempcapacityreserved=True,
            tempreservationtimestamp__lte=now - expiration_time
        )

        if expired_trips.exists():
            for trip in expired_trips:
                trip.tripcapacityremaining += trip.tempcapacitynumber
                trip.tempreservationtimestamp = None
                trip.tempcapacitynumber = 0
                trip.save()
                
                # Log each trip's release
                logger.info(f"Released expired temporary reservation for trip ID {trip.id}. "
                            f"Capacity restored: {trip.tempcapacitynumber}.")

            logger.info(f"Total of {len(expired_trips)} expired temporary trip reservations released.")
        else:
            logger.info("No expired temporary trip reservations found.")

    except Exception as e:
        logger.error(f"Error releasing expired trip reservations: {e}", exc_info=True)


def release_expired_room_reservations():
    """
    Releases expired temporary room reservations that were not finalized.
    """
    from .models import MmsTripRoom
    expiration_time = timedelta(minutes=5)
    now = timezone.now()
    print(now)

    try:
        expired_reservations = MmsTripRoom.objects.filter(
            tempreserved=True,
            tempreservationtimestamp__lt=now - expiration_time
        )

        if expired_reservations.exists():
            for room in expired_reservations:
                room.tempreserved = False
                room.tempreservationtimestamp = None
                room.tempreservationuser = None
                room.save()

                # Log each room's release
                logger.info(f"Released expired temporary reservation for room ID {room.id}. "
                            f"Reservation user: {room.tempreservationuser}, room number: {room.roomnumber}.")

            logger.info(f"Total of {len(expired_reservations)} expired temporary room reservations released.")
        else:
            logger.info("No expired temporary room reservations found.")

    except Exception as e:
        logger.error(f"Error releasing expired room reservations: {e}", exc_info=True)
