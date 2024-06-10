from django.urls import path
from .views import upload_photo, home, create_profile, profile, update, loginpage

urlpatterns = [
    path('upload_photo/', upload_photo, name='upload_photo'),
    path('home/', home, name='home'),
    path('login/', loginpage, name='login'),
    path('profile/<int:pk>', profile, name='profile'),
    path('update/<int:pk>', update, name='update'),
    path('create_profile/', create_profile, name='create_profile'),
]
