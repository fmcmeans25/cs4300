from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.DurationField(help_text="Running time, e.g. 02:15:00")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Seat(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"

    seat_number = models.CharField(max_length=10, unique=True)
    booking_status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.AVAILABLE
    )

    class Meta:
        ordering = ["seat_number"]

    def __str__(self):
        return f"Seat {self.seat_number} ({self.get_booking_status_display()})"


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booking_date"]
        constraints = [
            models.UniqueConstraint(fields=["movie", "seat"], name="unique_movie_seat")
        ]

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.seat.seat_number}"