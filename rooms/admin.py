from django.contrib import admindocs

# Register your models here.
list_display = ('room_number', 'room_type', 'price_per_night', 'capacity', 'beds', 'has_breakfast', 'is_available')
list_filter = ('room_type', 'has_breakfast', 'is_available')
search_fields = ('room_number', 'room_type')
list_editable = ('price_per_night', 'capacity', 'beds', 'has_breakfast', 'is_available')
list_per_page = 10


