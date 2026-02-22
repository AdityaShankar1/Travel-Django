import json
import requests
from ai_chat.services import get_ollama_response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Change these to point to the 'bookings' app
from bookings.models import Circuit, Booking
from bookings.forms import BookingForm

@csrf_exempt
def chat_view(request):
    # ... rest of your code ...
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')
            try:
                reply = get_ollama_response(prompt)
                return JsonResponse({'reply': reply})
            except Exception as e:
                return JsonResponse({'reply': f"Service Error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({'reply': f"Connection Error: {str(e)}"}, status=500)
    return JsonResponse({'reply': 'Invalid request'}, status=400)

def booking_list(request):
    circuits = Circuit.objects.all()
    return render(request, 'bookings/list.html', {'bookings': circuits})

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('home')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})