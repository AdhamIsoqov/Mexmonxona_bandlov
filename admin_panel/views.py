from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.contrib import messages
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto\'g\'ri!')
    
    return render(request, 'admin_panel/login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    rooms = Room.objects.all()
    total_rooms = rooms.count()
    available_rooms = rooms.filter(is_available=True).count()
    booked_rooms = rooms.filter(is_available=False).count()
    total_income = sum(room.price for room in rooms)
    
    return render(request, 'admin_panel/dashboard.html', {
        'rooms': rooms,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'booked_rooms': booked_rooms,
        'total_income': total_income
    })

@login_required(login_url='login')
def add_hotel(request):
    return render(request, 'admin_panel/add_hotel.html')

@login_required(login_url='login')
def add_room(request):
    if request.method == 'POST':
        try:
            room_number = request.POST.get('room_number')
            room_type = request.POST.get('room_type')
            price = request.POST.get('price')
            beds = request.POST.get('beds')
            capacity = request.POST.get('capacity')
            floor = request.POST.get('floor')
            description = request.POST.get('description')
            
            # Checkbox maydonlarini olish
            has_breakfast = request.POST.get('has_breakfast') == 'on'
            has_wifi = request.POST.get('has_wifi') == 'on'
            has_tv = request.POST.get('has_tv') == 'on'
            has_ac = request.POST.get('has_ac') == 'on'
            has_minibar = request.POST.get('has_minibar') == 'on'
            has_safe = request.POST.get('has_safe') == 'on'
            has_bathroom = request.POST.get('has_bathroom') == 'on'

            # Xona raqami allaqachon mavjudligini tekshirish
            if Room.objects.filter(room_number=room_number).exists():
                messages.error(request, f'Xona {room_number} allaqachon mavjud!')
                return render(request, 'admin_panel/add_room.html', {
                    'room_number': room_number,
                    'room_type': room_type,
                    'price': price,
                    'beds': beds,
                    'capacity': capacity,
                    'floor': floor,
                    'description': description,
                    'has_breakfast': has_breakfast,
                    'has_wifi': has_wifi,
                    'has_tv': has_tv,
                    'has_ac': has_ac,
                    'has_minibar': has_minibar,
                    'has_safe': has_safe,
                    'has_bathroom': has_bathroom,
                    'rooms': Room.objects.all().order_by('-id')
                })

            # Yangi xona yaratish
            room = Room.objects.create(
                room_number=room_number,
                room_type=room_type,
                price=price,
                beds=beds,
                capacity=capacity,
                floor=floor,
                description=description,
                has_breakfast=has_breakfast,
                has_wifi=has_wifi,
                has_tv=has_tv,
                has_ac=has_ac,
                has_minibar=has_minibar,
                has_safe=has_safe,
                has_bathroom=has_bathroom
            )
            
            messages.success(request, f'Xona {room_number} muvaffaqiyatli qo\'shildi!')
            return render(request, 'admin_panel/add_room.html', {
                'room_number': '',
                'room_type': '',
                'price': '',
                'beds': '',
                'capacity': '',
                'floor': '',
                'description': '',
                'has_breakfast': False,
                'has_wifi': False,
                'has_tv': False,
                'has_ac': False,
                'has_minibar': False,
                'has_safe': False,
                'has_bathroom': False,
                'rooms': Room.objects.all().order_by('-id')
            })
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return render(request, 'admin_panel/add_room.html', {
                'room_number': room_number,
                'room_type': room_type,
                'price': price,
                'beds': beds,
                'capacity': capacity,
                'floor': floor,
                'description': description,
                'has_breakfast': has_breakfast,
                'has_wifi': has_wifi,
                'has_tv': has_tv,
                'has_ac': has_ac,
                'has_minibar': has_minibar,
                'has_safe': has_safe,
                'has_bathroom': has_bathroom,
                'rooms': Room.objects.all().order_by('-id')
            })
    
    # GET so'rovi uchun barcha o'zgaruvchilarni boshlang'ich qiymatlar bilan qo'shamiz
    return render(request, 'admin_panel/add_room.html', {
        'room_number': '',
        'room_type': '',
        'price': '',
        'beds': '',
        'capacity': '',
        'floor': '',
        'description': '',
        'has_breakfast': False,
        'has_wifi': False,
        'has_tv': False,
        'has_ac': False,
        'has_minibar': False,
        'has_safe': False,
        'has_bathroom': False,
        'rooms': Room.objects.all().order_by('-id')
    })

@login_required(login_url='login')
def update_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        try:
            room_number = request.POST.get('room_number')
            room_type = request.POST.get('room_type')
            price = request.POST.get('price')
            beds = request.POST.get('beds')
            capacity = request.POST.get('capacity')
            floor = request.POST.get('floor')
            description = request.POST.get('description')
            
            # Checkbox maydonlarini olish
            has_breakfast = request.POST.get('has_breakfast') == 'on'
            has_wifi = request.POST.get('has_wifi') == 'on'
            has_tv = request.POST.get('has_tv') == 'on'
            has_ac = request.POST.get('has_ac') == 'on'
            has_minibar = request.POST.get('has_minibar') == 'on'
            has_safe = request.POST.get('has_safe') == 'on'
            has_bathroom = request.POST.get('has_bathroom') == 'on'

            # Xona raqami allaqachon mavjudligini tekshirish (o'zini hisobga olmasdan)
            if Room.objects.filter(room_number=room_number).exclude(id=room_id).exists():
                messages.error(request, f'Xona {room_number} allaqachon mavjud!')
                return render(request, 'admin_panel/add_room.html', {
                    'room': room,
                    'room_number': room_number,
                    'room_type': room_type,
                    'price': price,
                    'beds': beds,
                    'capacity': capacity,
                    'floor': floor,
                    'description': description,
                    'has_breakfast': has_breakfast,
                    'has_wifi': has_wifi,
                    'has_tv': has_tv,
                    'has_ac': has_ac,
                    'has_minibar': has_minibar,
                    'has_safe': has_safe,
                    'has_bathroom': has_bathroom,
                    'rooms': Room.objects.all().order_by('-id')
                })

            # Xona ma'lumotlarini yangilash
            room.room_number = room_number
            room.room_type = room_type
            room.price = price
            room.beds = beds
            room.capacity = capacity
            room.floor = floor
            room.description = description
            room.has_breakfast = has_breakfast
            room.has_wifi = has_wifi
            room.has_tv = has_tv
            room.has_ac = has_ac
            room.has_minibar = has_minibar
            room.has_safe = has_safe
            room.has_bathroom = has_bathroom
            room.save()
            
            messages.success(request, f'Xona {room_number} muvaffaqiyatli yangilandi!')
            return render(request, 'admin_panel/add_room.html', {
                'room': room,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'price': room.price,
                'beds': room.beds,
                'capacity': room.capacity,
                'floor': room.floor,
                'description': room.description,
                'has_breakfast': room.has_breakfast,
                'has_wifi': room.has_wifi,
                'has_tv': room.has_tv,
                'has_ac': room.has_ac,
                'has_minibar': room.has_minibar,
                'has_safe': room.has_safe,
                'has_bathroom': room.has_bathroom,
                'rooms': Room.objects.all().order_by('-id')
            })
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return render(request, 'admin_panel/add_room.html', {
                'room': room,
                'room_number': room_number,
                'room_type': room_type,
                'price': price,
                'beds': beds,
                'capacity': capacity,
                'floor': floor,
                'description': description,
                'has_breakfast': has_breakfast,
                'has_wifi': has_wifi,
                'has_tv': has_tv,
                'has_ac': has_ac,
                'has_minibar': has_minibar,
                'has_safe': has_safe,
                'has_bathroom': has_bathroom,
                'rooms': Room.objects.all().order_by('-id')
            })
    
    return render(request, 'admin_panel/add_room.html', {
        'room': room,
        'room_number': room.room_number,
        'room_type': room.room_type,
        'price': room.price,
        'beds': room.beds,
        'capacity': room.capacity,
        'floor': room.floor,
        'description': room.description,
        'has_breakfast': room.has_breakfast,
        'has_wifi': room.has_wifi,
        'has_tv': room.has_tv,
        'has_ac': room.has_ac,
        'has_minibar': room.has_minibar,
        'has_safe': room.has_safe,
        'has_bathroom': room.has_bathroom,
        'rooms': Room.objects.all().order_by('-id')
    })

@login_required(login_url='login')
def get_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        room_dict = model_to_dict(room)
        room_dict['is_available'] = room.is_available
        return JsonResponse(room_dict)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Xona topilmadi'}, status=404)

@login_required(login_url='login')
def view_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return render(request, 'admin_panel/view_room.html', {'room': room})
    except Room.DoesNotExist:
        messages.error(request, 'Xona topilmadi')
        return redirect('add_room')

@login_required(login_url='login')
def delete_room(request, room_id):
    if request.method == 'POST':
        try:
            room = Room.objects.get(id=room_id)
            room_number = room.room_number
            room.delete()
            return JsonResponse({
                'success': True,
                'message': f'{room_number} raqamli xona muvaffaqiyatli o\'chirildi'
            })
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Xona topilmadi'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Xatolik yuz berdi: {str(e)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'message': 'Noto\'g\'ri so\'rov'
    }, status=400)

@login_required(login_url='login')
def get_rooms(request):
    try:
        rooms = Room.objects.all().order_by('room_number')
        rooms_data = []
        for room in rooms:
            rooms_data.append({
                'id': room.id,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'is_available': room.is_available,
                'price': str(room.price),
                'beds': room.beds,
                'capacity': room.capacity,
                'floor': room.floor,
                'description': room.description,
                'has_breakfast': room.has_breakfast,
                'has_wifi': room.has_wifi,
                'has_tv': room.has_tv,
                'has_ac': room.has_ac,
                'has_minibar': room.has_minibar,
                'has_safe': room.has_safe,
                'has_bathroom': room.has_bathroom
            })
        return JsonResponse({'rooms': rooms_data})
    except Exception as e:
        return JsonResponse({
            'error': f'Xatolik yuz berdi: {str(e)}'
        }, status=500)