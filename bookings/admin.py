from django.contrib import admin
from .models import Place, Circuit, CircuitStop, Hotel, Booking, Package

class CircuitStopInline(admin.TabularInline):
    model = CircuitStop
    extra = 1

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    inlines = [CircuitStopInline]
    list_display = ('name', 'base_price', 'package') # Added 'package' to list view

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'circuit', 'hotel_tier', 'start_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'hotel_tier')

admin.site.register(Package)
admin.site.register(Place)
admin.site.register(Hotel)
