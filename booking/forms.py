from django import forms
from admin_panel.models import Booking
from .models import Contact, Subscriber

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
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

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise forms.ValidationError("Chiqish sanasi kirish sanasidan katta bo'lishi kerak!")

        if room and not room.is_available:
            raise forms.ValidationError("Bu xona hozircha band!")

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