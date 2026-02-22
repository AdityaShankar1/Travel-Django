from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from bookings.views import (
    booking_list,
    create_booking,
    my_bookings, # Now this will work because we added it above
    BookingViewSet,
    PlaceViewSet,
    CircuitViewSet,
    CircuitStopViewSet
)
from ai_chat.views import chat_view

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'circuits', CircuitViewSet)
router.register(r'circuit-stops', CircuitStopViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', booking_list, name='home'),
    path('chat/', chat_view, name='chat'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('book/<int:package_id>/', create_booking, name='create_booking'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('weather/', include('weather.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)