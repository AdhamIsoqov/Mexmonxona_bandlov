from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blog_details, name='blog_details'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('rooms-list/', views.rooms_list, name='rooms_list'),
    path('support/', views.support, name='support'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('click-payment/<int:booking_id>/', views.click_payment, name='click_payment'),
    path('click-callback/', views.click_callback, name='click_callback'),
] 