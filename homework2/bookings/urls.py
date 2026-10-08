from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("movies", views.MovieViewSet)
router.register("seats", views.SeatViewSet)
router.register("bookings", views.BookingViewSet, basename="booking")

urlpatterns = [
    # HTML pages
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking, name="seat_booking"),
    path("my-bookings/", views.booking_history, name="booking_history"),
    path("my-bookings/<int:booking_id>/cancel/", views.cancel_booking_view, name="cancel_booking"),
    # REST API
    path("api/", include(router.urls)),
]