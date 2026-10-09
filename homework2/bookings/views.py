from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import (
    BookingSerializer, BookSeatSerializer, MovieSerializer, SeatSerializer,
)
from .services import SeatUnavailable, book_seat, booked_seat_ids, cancel_booking


# --------------------------------------------------------------------------
# REST API (Django REST Framework viewsets)
# --------------------------------------------------------------------------
class MovieViewSet(viewsets.ModelViewSet):
    """Full CRUD on movies. Anyone can read; only admins can change."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAdminUser()]


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """Seat availability and booking.

    Use ``?movie=<id>`` to see availability for one movie, and
    ``?status=available`` (or ``booked``) to filter."""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _booked_ids_for_movie(self):
        """Seat ids booked for ?movie=<id>, or None when no movie was given."""
        movie_id = self.request.query_params.get("movie")
        if movie_id is None:
            return None
        if not movie_id.isdigit():
            raise ValidationError({"movie": "Must be a movie id."})
        return booked_seat_ids(int(movie_id))

    def get_queryset(self):
        qs = super().get_queryset()
        wanted = self.request.query_params.get("status")
        if not wanted:
            return qs
        booked = self._booked_ids_for_movie()
        if booked is None:  # no movie given: use the overall seat flag
            return qs.filter(booking_status=wanted)
        if wanted == Seat.Status.BOOKED:
            return qs.filter(id__in=booked)
        if wanted == Seat.Status.AVAILABLE:
            return qs.exclude(id__in=booked)
        return qs.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ("list", "retrieve"):
            context["booked_seat_ids"] = self._booked_ids_for_movie()
        return context

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        seat = self.get_object()
        form = BookSeatSerializer(data=request.data)
        form.is_valid(raise_exception=True)
        try:
            booking = book_seat(request.user, form.validated_data["movie"], seat)
        except SeatUnavailable as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Users book seats, view their own history, and cancel bookings."""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            "movie", "seat"
        )

    def perform_destroy(self, instance):
        cancel_booking(instance)


# --------------------------------------------------------------------------
# HTML pages (Django templates)
# --------------------------------------------------------------------------
def movie_list(request):
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})


@login_required
def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        seat_id = request.POST.get("seat", "")
        seat = Seat.objects.filter(pk=seat_id).first() if seat_id.isdigit() else None
        if seat is None:
            messages.error(request, "Please choose a seat.")
        else:
            try:
                book_seat(request.user, movie, seat)
            except SeatUnavailable as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, f"Booked seat {seat.seat_number} for {movie.title}.")
                return redirect("booking_history")

    taken = booked_seat_ids(movie.id)
    seats = list(Seat.objects.all())
    for seat in seats:
        seat.is_taken = seat.id in taken  # availability for THIS movie only

    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": seats})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


@login_required
@require_POST
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    cancel_booking(booking)
    messages.success(request, "Booking cancelled.")
    return redirect("booking_history")