from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='packages/', null=True, blank=True)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='places/', null=True, blank=True)

    def __str__(self):
        return self.name

class Circuit(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='circuits', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default="An amazing travel experience.")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='circuits/', null=True, blank=True)
    places = models.ManyToManyField(Place, through='CircuitStop')

    def __str__(self):
        pkg_name = self.package.name if self.package else "No Package"
        return f"{pkg_name} - {self.name}"

class CircuitStop(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

class Hotel(models.Model):
    HOTEL_TIERS = [('BUD', 'Budget'), ('STD', 'Standard'), ('PRM', 'Premium'), ('LUX', 'Luxury')]
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=3, choices=HOTEL_TIERS)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_tier_display()})"

class Booking(models.Model):
    TRANSPORT_CHOICES = [('CAB', 'Cab & Driver'), ('BUS', 'Group Bus'), ('TRN', 'Train')]
    HOTEL_TIERS = [('BUD', 'Budget'), ('STD', 'Standard'), ('PRM', 'Premium'), ('LUX', 'Luxury')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circuit = models.ForeignKey(Circuit, on_delete=models.PROTECT)
    hotel_tier = models.CharField(max_length=3, choices=HOTEL_TIERS)
    transport_choice = models.CharField(max_length=3, choices=TRANSPORT_CHOICES)
    start_date = models.DateField()
    duration_days = models.PositiveIntegerField(default=2)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        multipliers = {'BUD': 1.0, 'STD': 1.2, 'PRM': 1.5, 'LUX': 2.0}
        tier_multiplier = multipliers.get(self.hotel_tier, 1.0)
        base = float(self.circuit.base_price) * self.duration_days
        total = (base * tier_multiplier) * 1.18
        return round(total, 2)

    def __str__(self):
        return f"{self.user.username} - {self.circuit.name} ({self.start_date})"