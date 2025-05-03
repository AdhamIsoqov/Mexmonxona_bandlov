from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from admin_panel.models import Room, Booking
from .models import Contact, Subscriber
from .forms import BookingForm, ContactForm, SubscriberForm
from datetime import date

# Create your views here.

def index(request):
    rooms = Room.objects.filter(is_available=True)[:4]
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Siz muvaffaqiyatli obuna bo'ldingiz!")
            return redirect('index')
    else:
        form = SubscriberForm()
    return render(request, 'index.html', {'rooms': rooms, 'form': form})

def about_us(request):
    return render(request, 'about-us.html')

def blog(request):
    return render(request, 'blog.html')

def blog_details(request):
    return render(request, 'blog-details.html')

def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    today = date.today()
    active_booking = Booking.objects.filter(
        room=room,
        check_in_date__lte=today,
        check_out_date__gte=today,
        is_confirmed=True
    ).first()
    next_booking = Booking.objects.filter(
        room=room,
        check_in_date__gt=today,
        is_confirmed=True
    ).order_by('check_in_date').first()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.total_price = room.price * (booking.check_out_date - booking.check_in_date).days
            booking.save()
            room.is_available = False
            room.save()
            messages.success(request, f"Xona {room.room_number} {booking.check_in_date} dan {booking.check_out_date} gacha muvaffaqiyatli band qilindi!")
            return redirect('room_details', room_id=room.id)
    else:
        form = BookingForm(initial={'room': room})
    return render(request, 'room_details.html', {
        'room': room,
        'form': form,
        'active_booking': active_booking,
        'next_booking': next_booking,
    })

def booking(request):
    available_rooms = Room.objects.filter(is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.total_price = booking.room.price * (booking.check_out_date - booking.check_in_date).days
            booking.save()
            messages.success(request, "Bandlov muvaffaqiyatli amalga oshirildi!")
            return redirect('booking')
    else:
        form = BookingForm()
    return render(request, 'booking.html', {
        'form': form,
        'rooms': available_rooms
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_list.html', {'rooms': rooms})

def support(request):
    return render(request, 'support.html')
