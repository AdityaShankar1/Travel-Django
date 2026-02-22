from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here
from django.contrib.auth.models import User
from .models import Package, Circuit, Booking

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.pkg = Package.objects.create(name="Heritage")
        self.circuit = Circuit.objects.create(
            name="Madurai",
            base_price=1000.00,
            package=self.pkg
        )

    def test_price_calculation(self):
        # Create a 2-day booking, Premium tier (multiplier 1.5)
        # Formula: (1000 * 2) * 1.5 * 1.18 (tax) = 3540.0
        booking = Booking.objects.create(
            user=self.user,
            circuit=self.circuit,
            hotel_tier='PRM',
            start_date='2026-03-01',
            duration_days=2
        )
        self.assertEqual(booking.calculate_total_price(), 3540.00)