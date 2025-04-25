from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# Xona modeli
class Room(models.Model):
    ROOM_TYPES = [
        ("ST", "Standart"),
        ("CF", "Komfort"),
        ("LX", "Lyuks"),
    ]

    room_number = models.CharField(max_length=10, verbose_name="Xona raqami", unique=True)
    room_type = models.CharField(
        max_length=2,
        choices=ROOM_TYPES,
        default="ST",
        verbose_name="Xona turi"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Narxi",
        default=0.00
    )
    beds = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Karavotlar soni",
        default=1
    )
    capacity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Sig'imi",
        default=1
    )
    floor = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Qavat",
        default=1
    )
    description = models.TextField(
        verbose_name="Tavsif",
        blank=True,
        null=True
    )
    has_breakfast = models.BooleanField(
        default=False,
        verbose_name="Nonushta"
    )
    has_wifi = models.BooleanField(
        default=False,
        verbose_name="Wi-Fi"
    )
    has_tv = models.BooleanField(
        default=False,
        verbose_name="Televizor"
    )
    has_ac = models.BooleanField(
        default=False,
        verbose_name="Konditsioner"
    )
    has_minibar = models.BooleanField(
        default=False,
        verbose_name="Minibar"
    )
    has_safe = models.BooleanField(
        default=False,
        verbose_name="Seif"
    )
    has_bathroom = models.BooleanField(
        default=False,
        verbose_name="Hammom"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Mavjud"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        ordering = ['room_number']

    def __str__(self):
        return f"Xona {self.room_number}"

    def save(self, *args, **kwargs):
        if Room.objects.filter(room_number=self.room_number).exclude(id=self.id).exists():
            raise ValueError(f"Xona {self.room_number} allaqachon mavjud!")
        super().save(*args, **kwargs)

class Booking(models.Model):
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE,
        verbose_name="Xona"
    )
    guest_name = models.CharField(
        max_length=100,
        verbose_name="Mehmon ismi"
    )
    guest_email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True
    )
    guest_phone = models.CharField(
        max_length=20,
        verbose_name="Telefon raqami",
        blank=True,
        null=True
    )
    check_in_date = models.DateField(
        verbose_name="Kirish sanasi"
    )
    check_out_date = models.DateField(
        verbose_name="Chiqish sanasi"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Umumiy narx"
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Tasdiqlangan"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )

    class Meta:
        verbose_name = "Bandlov"
        verbose_name_plural = "Bandlovlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.guest_name} - {self.room.room_number} ({self.check_in_date} - {self.check_out_date})"

    def clean(self):
        from django.core.exceptions import ValidationError
        from datetime import date, timedelta

        # Hozirgidan oldingi kunni tanlashni taqiqlash
        if self.check_in_date < date.today():
            raise ValidationError("Siz hozirgidan oldingi kunni tanlashingiz mumkin emas!")

        # Booking muddatini tekshirish (1-7 kun)
        days = (self.check_out_date - self.check_in_date).days
        if days < 1:
            raise ValidationError("Bandlov muddati kamida 1 kun bo'lishi kerak!")
        if days > 7:
            raise ValidationError("Bandlov muddati ko'pi bilan 7 kun bo'lishi mumkin!")

        # Xonaning band bo'lmaganligini tekshirish
        if Booking.objects.filter(
            room=self.room,
            check_in_date__lte=self.check_out_date,
            check_out_date__gte=self.check_in_date,
            is_confirmed=True
        ).exclude(id=self.id).exists():
            raise ValidationError("Bu xona tanlangan vaqtda band!")

    def save(self, *args, **kwargs):
        # Umumiy narxni hisoblash
        days = (self.check_out_date - self.check_in_date).days
        self.total_price = self.room.price * days
        super().save(*args, **kwargs)