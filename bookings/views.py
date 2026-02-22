from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Booking, Place, Circuit, CircuitStop, Package
from .serializers import (
    BookingSerializer, PlaceSerializer, CircuitSerializer, CircuitStopSerializer
)
from .forms import BookingForm


# --- Web UI Views ---

def booking_list(request):
    """Lists all available packages with optional search."""
    query = request.GET.get('q')
    packages = Package.objects.all()

    if query:
        # Search by package name or description
        packages = packages.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'bookings/list.html', {'packages': packages, 'query': query})


@login_required
def create_booking(request, package_id):
    """Handles booking creation filtered by the selected package."""
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, package=package)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(package=package)

    return render(request, 'bookings/create_booking.html', {'form': form, 'package': package})


@login_required
def my_bookings(request):
    """Shows all bookings for the logged-in user."""
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': user_bookings})


# --- API ViewSets ---

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminOrReadOnly]


class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer
    permission_classes = [IsAdminOrReadOnly]


class CircuitStopViewSet(viewsets.ModelViewSet):
    queryset = CircuitStop.objects.all()
    serializer_class = CircuitStopSerializer
    permission_classes = [IsAdminOrReadOnly]