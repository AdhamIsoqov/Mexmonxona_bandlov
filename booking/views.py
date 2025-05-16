from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from admin_panel.models import Room, Booking, Invoice
from .models import Contact, Subscriber
from .forms import BookingForm, ContactForm, SubscriberForm
from datetime import date
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
            booking.is_confirmed = True
            booking.save()
            # Xona mavjudligini yangilash
            booking.room.is_available = False
            booking.room.save()
            # Invoice yaratish
            invoice, created = Invoice.objects.get_or_create(
                booking=booking,
                defaults={'amount': booking.total_price}
            )
            # Click to'lov sahifasiga yo'naltirish
            return redirect('click_payment', booking_id=booking.id)
    else:
        form = BookingForm(initial={'room': room})
    # To'lanmagan invoice mavjudligini tekshirish
    unpaid_invoice = Invoice.objects.filter(
        booking__room=room,
        paid=False
    ).first()
    return render(request, 'room_details.html', {
        'room': room,
        'form': form,
        'active_booking': active_booking,
        'next_booking': next_booking,
        'unpaid_invoice': unpaid_invoice,
    })

def booking(request):
    available_rooms = Room.objects.filter(is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.total_price = booking.room.price * (booking.check_out_date - booking.check_in_date).days
            booking.is_confirmed = True
            booking.save()
            # Xona mavjudligini yangilash
            booking.room.is_available = False
            booking.room.save()
            # Invoice yaratish va to'lovga yo'naltirish
            invoice, created = Invoice.objects.get_or_create(
                booking=booking,
                defaults={'amount': booking.total_price}
            )
            return redirect('click_payment', booking_id=booking.id)
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

@login_required
def click_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    invoice = get_object_or_404(Invoice, booking=booking)
    # Click to'lov formasi uchun ma'lumotlar
    callback_url = request.build_absolute_uri(reverse('click_callback'))
    return_url = request.build_absolute_uri(reverse('room_details', args=[booking.id]))
    context = {
        'click_url': 'https://my.click.uz/services/pay',
        'merchant_id': settings.CLICK_MERCHANT_ID,
        'service_id': settings.CLICK_SERVICE_ID,
        'amount': invoice.amount,
        'trans_id': invoice.invoice_number,
        'return_url': return_url,
        'callback_url': callback_url,
    }
    return render(request, 'payment.html', context)

@csrf_exempt
def click_callback(request):
    trans_id = request.POST.get('trans_id') or request.GET.get('trans_id')
    invoice = get_object_or_404(Invoice, invoice_number=trans_id)
    # To'lov muvaffaqiyatli deb belgilash
    invoice.paid = True
    invoice.generate_pdf()
    invoice.save()
    return HttpResponse('SUCCESS')
