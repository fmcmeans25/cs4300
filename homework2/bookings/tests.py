from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Booking, Movie, Seat


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
