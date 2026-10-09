from datetime import date, timedelta

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat


class Command(BaseCommand):
    help = "Create demo seats and movies if the database is empty (safe to re-run)."

    def handle(self, *args, **options):
        if not Seat.objects.exists():
            seats = [Seat(seat_number=f"{row}{n}") for row in "ABCD" for n in range(1, 6)]
            Seat.objects.bulk_create(seats)
            self.stdout.write(f"Created {len(seats)} seats")
        if not Movie.objects.exists():
            Movie.objects.bulk_create([
                Movie(title="Dune", description="A noble family takes control of a desert planet.",
                      release_date=date(2021, 10, 22), duration=timedelta(hours=2, minutes=35)),
                Movie(title="Arrival", description="A linguist works to communicate with alien visitors.",
                      release_date=date(2016, 11, 11), duration=timedelta(hours=1, minutes=56)),
                Movie(title="Spirited Away", description="A girl wanders into a world of spirits.",
                      release_date=date(2001, 7, 20), duration=timedelta(hours=2, minutes=5)),
            ])
            self.stdout.write("Created 3 movies")