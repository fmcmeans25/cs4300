from datetime import date, timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Booking, Movie, Seat
from .services import SeatUnavailable, book_seat, cancel_booking


class BookingFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("fran", password="pw12345!")
        self.admin = User.objects.create_superuser("root", password="pw12345!")
        self.movie = Movie.objects.create(
            title="Dune", description="Sand.", release_date=date(2021, 10, 22),
            duration=timedelta(hours=2, minutes=35),
        )
        self.seat = Seat.objects.create(seat_number="A1")
        self.api = APIClient()

    # --- API ---------------------------------------------------------
    def test_movies_public_read_admin_write(self):
        self.assertEqual(self.api.get("/api/movies/").status_code, 200)
        payload = {"title": "X", "description": "", "release_date": "2024-01-01", "duration": "01:30:00"}
        self.api.force_authenticate(self.user)
        self.assertEqual(self.api.post("/api/movies/", payload).status_code, 403)
        self.api.force_authenticate(self.admin)
        self.assertEqual(self.api.post("/api/movies/", payload).status_code, 201)

    def test_seat_availability_filter(self):
        Seat.objects.create(seat_number="A2", booking_status=Seat.Status.BOOKED)
        data = self.api.get("/api/seats/?status=available").json()
        self.assertEqual([s["seat_number"] for s in data], ["A1"])

    def test_book_seat_action_and_double_booking(self):
        self.api.force_authenticate(self.user)
        url = f"/api/seats/{self.seat.id}/book/"
        self.assertEqual(self.api.post(url, {"movie": self.movie.id}).status_code, 201)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, Seat.Status.BOOKED)
        self.assertEqual(self.api.post(url, {"movie": self.movie.id}).status_code, 409)

    def test_booking_create_history_and_cancel(self):
        self.api.force_authenticate(self.user)
        r = self.api.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["user"], "fran")
        self.assertEqual(len(self.api.get("/api/bookings/").json()), 1)
        self.assertEqual(self.api.delete(f"/api/bookings/{r.json()['id']}/").status_code, 204)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, Seat.Status.AVAILABLE)

    def test_users_only_see_own_bookings(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.admin)
        self.api.force_authenticate(self.user)
        self.assertEqual(self.api.get("/api/bookings/").json(), [])

    def test_bookings_require_login(self):
        self.assertIn(self.api.get("/api/bookings/").status_code, (401, 403))

    # --- HTML pages --------------------------------------------------
    def test_movie_list_page(self):
        self.assertContains(self.client.get("/"), "Dune")

    def test_seat_booking_page_requires_login(self):
        r = self.client.get(f"/movies/{self.movie.id}/book/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r["Location"])

    def test_book_through_html_then_see_history(self):
        self.client.login(username="fran", password="pw12345!")
        r = self.client.post(f"/movies/{self.movie.id}/book/", {"seat": self.seat.id})
        self.assertRedirects(r, "/my-bookings/")
        self.assertContains(self.client.get("/my-bookings/"), "A1")
        self.client.post(f"/my-bookings/{Booking.objects.get().id}/cancel/")
        self.assertEqual(Booking.objects.count(), 0)


# ----------------------------------------------------------------------
# Unit tests: models and business logic in isolation
# ----------------------------------------------------------------------
class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("fran", password="pw12345!")
        self.movie = Movie.objects.create(
            title="Dune", release_date=date(2021, 10, 22), duration=timedelta(hours=2, minutes=35)
        )
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_str_is_title(self):
        self.assertEqual(str(self.movie), "Dune")

    def test_movies_ordered_by_title(self):
        Movie.objects.create(title="Arrival", release_date=date(2016, 11, 11), duration=timedelta(hours=1, minutes=56))
        self.assertEqual([m.title for m in Movie.objects.all()], ["Arrival", "Dune"])

    def test_seat_defaults_to_available(self):
        self.assertEqual(self.seat.booking_status, Seat.Status.AVAILABLE)

    def test_seat_str_shows_number_and_status(self):
        self.assertEqual(str(self.seat), "Seat A1 (Available)")

    def test_seat_number_must_be_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Seat.objects.create(seat_number="A1")

    def test_booking_date_is_set_automatically(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertIsNotNone(booking.booking_date)

    def test_booking_str(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertEqual(str(booking), "fran - Dune - A1")

    def test_same_seat_cannot_be_booked_twice_for_one_movie(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)

    def test_deleting_movie_deletes_its_bookings(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.movie.delete()
        self.assertEqual(Booking.objects.count(), 0)


class ServiceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("fran", password="pw12345!")
        self.movie = Movie.objects.create(
            title="Dune", release_date=date(2021, 10, 22), duration=timedelta(hours=2, minutes=35)
        )
        self.seat = Seat.objects.create(seat_number="A1")

    def test_book_seat_creates_booking_and_marks_seat_booked(self):
        booking = book_seat(self.user, self.movie, self.seat)
        self.seat.refresh_from_db()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(self.seat.booking_status, Seat.Status.BOOKED)

    def test_book_seat_rejects_a_taken_seat(self):
        book_seat(self.user, self.movie, self.seat)
        with self.assertRaises(SeatUnavailable):
            book_seat(self.user, self.movie, self.seat)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_booking_frees_the_seat(self):
        booking = book_seat(self.user, self.movie, self.seat)
        cancel_booking(booking)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, Seat.Status.AVAILABLE)
        self.assertEqual(Booking.objects.count(), 0)


class SeedDemoCommandTests(TestCase):
    def run_seed(self):
        out = StringIO()
        call_command("seed_demo", stdout=out)
        return out.getvalue()

    def test_creates_demo_seats_and_movies_when_empty(self):
        output = self.run_seed()
        self.assertEqual(Seat.objects.count(), 20)
        self.assertEqual(Movie.objects.count(), 3)
        self.assertIn("Created 20 seats", output)
        self.assertIn("Created 3 movies", output)

    def test_is_safe_to_run_twice(self):
        self.run_seed()
        self.run_seed()
        self.assertEqual(Seat.objects.count(), 20)
        self.assertEqual(Movie.objects.count(), 3)

    def test_does_not_touch_existing_data(self):
        Seat.objects.create(seat_number="Z9")
        Movie.objects.create(title="Mine", release_date=date(2020, 1, 1), duration=timedelta(hours=1))
        self.run_seed()
        self.assertEqual(Seat.objects.count(), 1)
        self.assertEqual(Movie.objects.count(), 1)


class PerMovieAvailabilityTests(TestCase):
    """The same seat can be booked for different movies, but only once per movie."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("fran", password="pw12345!")
        self.other = User.objects.create_user("sam", password="pw12345!")
        self.dune = Movie.objects.create(
            title="Dune", release_date=date(2021, 10, 22), duration=timedelta(hours=2, minutes=35)
        )
        self.arrival = Movie.objects.create(
            title="Arrival", release_date=date(2016, 11, 11), duration=timedelta(hours=1, minutes=56)
        )
        self.seat = Seat.objects.create(seat_number="B3")
        self.api = APIClient()

    def test_same_seat_can_be_booked_for_two_different_movies(self):
        book_seat(self.user, self.dune, self.seat)
        book_seat(self.other, self.arrival, self.seat)
        self.assertEqual(Booking.objects.filter(seat=self.seat).count(), 2)

    def test_same_seat_cannot_be_booked_twice_for_the_same_movie(self):
        book_seat(self.user, self.dune, self.seat)
        with self.assertRaises(SeatUnavailable):
            book_seat(self.other, self.dune, self.seat)

    def test_cancelling_one_movie_keeps_seat_flag_while_another_booking_remains(self):
        first = book_seat(self.user, self.dune, self.seat)
        book_seat(self.other, self.arrival, self.seat)
        cancel_booking(first)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, Seat.Status.BOOKED)

    def test_api_booking_same_seat_for_second_movie_succeeds(self):
        self.api.force_authenticate(self.user)
        url = f"/api/seats/{self.seat.id}/book/"
        self.assertEqual(self.api.post(url, {"movie": self.dune.id}).status_code, 201)
        self.assertEqual(self.api.post(url, {"movie": self.arrival.id}).status_code, 201)
        self.assertEqual(self.api.post(url, {"movie": self.arrival.id}).status_code, 409)

    def test_api_seat_list_reports_status_for_the_requested_movie(self):
        book_seat(self.user, self.dune, self.seat)
        dune = self.api.get(f"/api/seats/?movie={self.dune.id}").json()
        arrival = self.api.get(f"/api/seats/?movie={self.arrival.id}").json()
        self.assertEqual(dune[0]["booking_status"], "booked")
        self.assertEqual(arrival[0]["booking_status"], "available")

    def test_api_status_filter_applies_per_movie(self):
        book_seat(self.user, self.dune, self.seat)
        free_dune = self.api.get(f"/api/seats/?movie={self.dune.id}&status=available").json()
        free_arrival = self.api.get(f"/api/seats/?movie={self.arrival.id}&status=available").json()
        booked_dune = self.api.get(f"/api/seats/?movie={self.dune.id}&status=booked").json()
        self.assertEqual(free_dune, [])
        self.assertEqual(len(free_arrival), 1)
        self.assertEqual(len(booked_dune), 1)

    def test_api_rejects_a_non_numeric_movie_filter(self):
        self.assertEqual(self.api.get("/api/seats/?movie=abc").status_code, 400)

    def test_api_unknown_status_with_movie_returns_nothing(self):
        self.assertEqual(self.api.get(f"/api/seats/?movie={self.dune.id}&status=nope").json(), [])

    def test_seat_page_only_greys_out_seats_taken_for_that_movie(self):
        book_seat(self.other, self.dune, self.seat)
        self.client.login(username="fran", password="pw12345!")
        dune_page = self.client.get(f"/movies/{self.dune.id}/book/").content.decode()
        arrival_page = self.client.get(f"/movies/{self.arrival.id}/book/").content.decode()
        self.assertIn("disabled", dune_page)
        self.assertNotIn("disabled", arrival_page)

    def test_booking_same_seat_for_second_movie_through_html(self):
        self.client.login(username="fran", password="pw12345!")
        self.client.post(f"/movies/{self.dune.id}/book/", {"seat": self.seat.id})
        r = self.client.post(f"/movies/{self.arrival.id}/book/", {"seat": self.seat.id})
        self.assertRedirects(r, "/my-bookings/")
        self.assertEqual(Booking.objects.filter(user__username="fran").count(), 2)