from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def chat(request):
    # Chatga faqat login qilganlar kirishi uchun
    if not request.user.is_authenticated:
        return redirect("login_user")
    return render(request, "chat.html")

def logout_user(request):
    logout(request)
    return redirect("index")