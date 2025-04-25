from django.db import models
from admin_panel.models import Room, Booking

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aloqa"
        verbose_name_plural = "Aloqalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Obunachi"
        verbose_name_plural = "Obunachilar"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
