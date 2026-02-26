from django.contrib import admin
from django.urls import path
from umumiy.views import login_user, index, chat, logout_user, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), # Asosiy sahifa
    path('login/', login_user, name='login_user'),
    path('chat/', chat, name='chat'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register, name='register_user'),
]