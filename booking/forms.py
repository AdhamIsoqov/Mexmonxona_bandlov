from django import forms
from admin_panel.models import Booking as _Booking
from datetime import date as _date
from .models import Contact, Subscriber

class BookingForm(forms.ModelForm):
    class Meta:
        model = _Booking
        fields = ['room', 'guest_name', 'guest_email', 'guest_phone', 'check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingiz'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqamingiz'}),
            'room': forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        room = cleaned_data.get('room')

        # Sana tekshirish: bugungi kundan oldin bo'lmasligi va 1-7 kun oralig'ida bo'lishi
        if check_in_date and check_out_date:
            if check_in_date < _date.today():
                raise forms.ValidationError("Kirish sanasi bugungi kundan oldin bo'lmasligi kerak!")
            if check_in_date >= check_out_date:
                raise forms.ValidationError("Chiqish sanasi kirish sanasidan katta bo'lishi kerak!")
            days = (check_out_date - check_in_date).days
            if days < 1 or days > 7:
                raise forms.ValidationError("Bandlov muddati 1 dan 7 kungacha bo'lishi kerak!")

        # Band bo'lgan sanalar va qo'shni kunlarni tekshirish
        if room and check_in_date and check_out_date:
            exists = _Booking.objects.filter(
                room=room,
                check_in_date__lte=check_out_date,
                check_out_date__gte=check_in_date,
                is_confirmed=True
            ).exclude(id=getattr(self.instance, 'id', None)).exists()
            if exists:
                raise forms.ValidationError("Tanlangan sanalar oralig'ida yoki unga qo'shni kunlarda xona band!")

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingiz'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Xabar mavzusi'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Xabaringiz'})
        }

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingiz'})
        } 