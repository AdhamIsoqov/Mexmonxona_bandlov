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