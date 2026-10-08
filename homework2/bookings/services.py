"""Booking business logic shared by the REST API and the HTML views."""
from django.db import transaction

from .models import Booking, Seat


class SeatUnavailable(Exception):
    pass


@transaction.atomic
def book_seat(user, movie, seat):
    # Lock the seat row so two people can't grab it at the same moment.
    seat = Seat.objects.select_for_update().get(pk=seat.pk)
    if seat.booking_status != Seat.Status.AVAILABLE:
        raise SeatUnavailable(f"Seat {seat.seat_number} is already booked.")
    booking = Booking.objects.create(user=user, movie=movie, seat=seat)
    seat.booking_status = Seat.Status.BOOKED
    seat.save(update_fields=["booking_status"])
    return booking


@transaction.atomic
def cancel_booking(booking):
    seat = Seat.objects.select_for_update().get(pk=booking.seat_id)
    booking.delete()
    seat.booking_status = Seat.Status.AVAILABLE
    seat.save(update_fields=["booking_status"])