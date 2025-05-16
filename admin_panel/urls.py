from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add_hotel/", views.add_hotel, name="add_hotel"),
    path("add-room/", views.add_room, name="add_room"),
    path("update-room/<int:room_id>/", views.update_room, name="update_room"),
    path('get-room/<int:room_id>/', views.get_room, name='get_room'),
    path('get-rooms/', views.get_rooms, name='get_rooms'),
    path('view-room/<int:room_id>/', views.view_room, name='view_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('invoices/', views.invoices_list, name='invoices_list'),
]
