from rest_framework import serializers

from .models import Booking, Movie, Seat
from .services import SeatUnavailable, book_seat


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    """When the view passes ``booked_seat_ids`` (i.e. ``?movie=<id>`` was given),
    ``booking_status`` is reported for that movie instead of the overall flag."""

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "booking_status"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        booked = self.context.get("booked_seat_ids")
        if booked is not None:
            data["booking_status"] = (
                Seat.Status.BOOKED if instance.id in booked else Seat.Status.AVAILABLE
            )
        return data


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