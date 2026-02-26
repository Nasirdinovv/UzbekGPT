from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from umumiy.models import UserProfile


def index(request):
    # Bu yerda hech qanday redirect kerak emas, shunchaki index.html ni ochamiz
    return render(request, "index.html")

def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")
        
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Django default User modelida username ishlatadi
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index") # Login bo'lgach indexga qaytadi
        else:
            messages.error(request, "Email yoki parol noto'g'ri")
            return redirect("login_user")
    
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("index")

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password2")

        if password != password_confirm:
            messages.error(request, "Parollar mos kelmadi")
            return redirect("register_user")

        
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan")
            return redirect("register_user")
        try:
            # UserProfile orqali foydalanuvchi yaratish
            new_user = UserProfile.objects.create_user(
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name,
            )
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return render(request, "register.html")

        except Exception as e:
            messages.error(request, f"Xatolik: {e}")
            return redirect("register_user")

    return render(request, "register.html")

def chat(request):
    # Chatga faqat login qilganlar kirishi uchun
    if not request.user.is_authenticated:
        return redirect("login_user")
    return render(request, "chat.html")
