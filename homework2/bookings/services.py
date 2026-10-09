"""Booking business logic shared by the REST API and the HTML views.

A seat is available for a movie unless a Booking already exists for that
(movie, seat) pair. ``Seat.booking_status`` is an overall flag: "booked" while
the seat has at least one booking, "available" when it has none.
"""
from django.db import transaction

from .models import Booking, Seat


class SeatUnavailable(Exception):
    pass


def booked_seat_ids(movie_id):
    """IDs of the seats already booked for the given movie."""
    return set(Booking.objects.filter(movie_id=movie_id).values_list("seat_id", flat=True))


@transaction.atomic
def book_seat(user, movie, seat):
    # Lock the seat row so two people can't grab it for the same movie at once.
    seat = Seat.objects.select_for_update().get(pk=seat.pk)
    if Booking.objects.filter(movie=movie, seat=seat).exists():
        raise SeatUnavailable(
            f"Seat {seat.seat_number} is already booked for {movie.title}."
        )
    booking = Booking.objects.create(user=user, movie=movie, seat=seat)
    if seat.booking_status != Seat.Status.BOOKED:
        seat.booking_status = Seat.Status.BOOKED
        seat.save(update_fields=["booking_status"])
    return booking


@transaction.atomic
def cancel_booking(booking):
    seat = Seat.objects.select_for_update().get(pk=booking.seat_id)
    booking.delete()
    # Only mark the seat free overall if no other movie still has it booked.
    if not Booking.objects.filter(seat=seat).exists():
        seat.booking_status = Seat.Status.AVAILABLE
        seat.save(update_fields=["booking_status"])