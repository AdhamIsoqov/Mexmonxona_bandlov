from django.db import models

from django.db import models

class Rooms(models.Model):
    Room_ID = models.AutoField(primary_key=True)
    Room_Type = models.CharField(max_length=20, choices=[
        ('Standart', 'Standart'),
        ('Lyuks', 'Lyuks'),
        ('Premium', 'Premium'),
    ])  # Xona turi (Standart, Lyuks, Premium)
    Room_Floor = models.IntegerField()
    Room_Number = models.IntegerField()
    Capacity = models.IntegerField(default=1)  # Xona sig'imi (necha kishi sig'ishi)
    View = models.CharField(max_length=100, blank=True, null=True)  # Xona manzarasi (masalan, dengiz, shahar)
    Is_Available = models.BooleanField(default=True)  # Xona band yoki bo'shligi

    def __str__(self):
        return f"Xona {self.Room_ID} ({self.Room_Type})"
      
class DailyRoomRates(models.Model):
    Day_Date = models.DateField()
    Room_ID = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    Daily_Room_Rate = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = ('Day_Date', 'Room_ID')

    def __str__(self):
        return f"{self.Room_ID} - {self.Day_Date} - {self.Daily_Room_Rate}"