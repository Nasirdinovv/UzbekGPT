from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.utils.safestring import mark_safe
from django.contrib import messages
 
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")

        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return render(request, "chat.html")
            print("user mavjud")
        else:
            messages.error(request, "Email yoki parol noto'g'ri")
            print("user mavjud emas")
            return redirect("login_user")
    else:
     return render(request, "login.html")

def index(request):
   return render(request, "index.html")

def logout_user(request):
    logout(request)
    return redirect("login_user")