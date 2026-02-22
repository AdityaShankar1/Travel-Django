# bookings/serializers.py
from rest_framework import serializers
from .models import Booking, Place, Circuit, CircuitStop


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class CircuitStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitStop
        fields = '__all__'


class CircuitSerializer(serializers.ModelSerializer):
    # This allows you to see the actual places nested within the circuit
    places = PlaceSerializer(many=True, read_only=True)

    class Meta:
        model = Circuit
        fields = ['id', 'name', 'base_price', 'places']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'circuit', 'hotel_tier', 'transport_choice', 'start_date']
        # 'is_confirmed' is removed so users can't override it via POST/PUT