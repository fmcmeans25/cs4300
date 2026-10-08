from rest_framework import serializers

from .models import Booking, Movie, Seat
from .services import SeatUnavailable, book_seat


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "booking_status"]


class BookSeatSerializer(serializers.Serializer):
    """Input for POST /api/seats/<id>/book/."""
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "user", "booking_date"]
        read_only_fields = ["booking_date"]

    def create(self, validated_data):
        try:
            return book_seat(
                self.context["request"].user,
                validated_data["movie"],
                validated_data["seat"],
            )
        except SeatUnavailable as exc:
            raise serializers.ValidationError({"seat": str(exc)})