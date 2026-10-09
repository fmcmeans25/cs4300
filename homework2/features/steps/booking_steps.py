from datetime import date, timedelta

from behave import given, then, when
from django.contrib.auth import get_user_model

from bookings.models import Booking, Movie, Seat
from bookings.services import book_seat

PASSWORD = "pw12345!"


def _movie(title):
    return Movie.objects.get(title=title)


# ---- Given ------------------------------------------------------------
@given('a movie called "{title}"')
def given_movie(context, title):
    Movie.objects.create(
        title=title, description="", release_date=date(2024, 1, 1),
        duration=timedelta(hours=2),
    )


@given('an available seat "{number}"')
def given_available_seat(context, number):
    Seat.objects.create(seat_number=number)


@given('a booked seat "{number}"')
def given_booked_seat(context, number):
    Seat.objects.create(seat_number=number, booking_status=Seat.Status.BOOKED)


@given('I am logged in as "{username}"')
def given_logged_in(context, username):
    context.user = get_user_model().objects.create_user(username, password=PASSWORD)
    context.test.client.login(username=username, password=PASSWORD)


@given("I am logged in as an admin")
def given_admin(context):
    context.user = get_user_model().objects.create_superuser("root", password=PASSWORD)
    context.test.client.login(username="root", password=PASSWORD)


@given("I am not logged in")
def given_anonymous(context):
    context.test.client.logout()


@given('I have booked seat "{number}" for "{title}"')
def given_booking(context, number, title):
    book_seat(context.user, _movie(title), Seat.objects.get(seat_number=number))


# ---- When -------------------------------------------------------------
@when("I open the movie list page")
def when_movie_list(context):
    context.response = context.test.client.get("/")


@when('I book seat "{number}" for "{title}"')
def when_book(context, number, title):
    seat = Seat.objects.get(seat_number=number)
    context.response = context.test.client.post(
        f"/movies/{_movie(title).id}/book/", {"seat": seat.id}, follow=True
    )


@when("I open my booking history")
def when_history(context):
    context.response = context.test.client.get("/my-bookings/")


@when('I cancel my booking for seat "{number}"')
def when_cancel(context, number):
    booking = Booking.objects.get(seat__seat_number=number, user=context.user)
    context.response = context.test.client.post(
        f"/my-bookings/{booking.id}/cancel/", follow=True
    )


@when('I try to open the booking page for "{title}"')
def when_open_booking_page(context, title):
    context.response = context.test.client.get(f"/movies/{_movie(title).id}/book/")


@when('I try to create the movie "{title}" through the API')
def when_api_create_movie(context, title):
    context.response = context.test.client.post(
        "/api/movies/",
        {"title": title, "description": "", "release_date": "2024-01-01", "duration": "01:30:00"},
        content_type="application/json",
    )


# ---- Then -------------------------------------------------------------
@then('I should see "{text}"')
def then_see(context, text):
    context.test.assertContains(context.response, text)


@then('seat "{number}" should be {status}')
def then_seat_status(context, number, status):
    seat = Seat.objects.get(seat_number=number)
    context.test.assertEqual(seat.booking_status, status)


@then("I should have {count:d} bookings")
def then_booking_count(context, count):
    context.test.assertEqual(Booking.objects.count(), count)


@then("I should be redirected to the login page")
def then_login_redirect(context):
    context.test.assertEqual(context.response.status_code, 302)
    context.test.assertIn("/accounts/login/", context.response["Location"])


@then("the response status should be {code:d}")
def then_status(context, code):
    context.test.assertEqual(context.response.status_code, code)