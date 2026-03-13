from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from httpx import request
from umumiy.models import UserProfile, Ai_agent, History
from main import chat_agent
from API_KEY import API_KEY
from google import genai

client = genai.Client(api_key=API_KEY)

def chat_agent(role = "oddiy suhbatdosh", message = "Sen nimalar gila olasan?"):

    contents = f"""

        SEN BU ROLDAGI {role} PROFESSIONAL SUXBATDOSHSAN. fagat shu mavzudagi savollarga javob gaytarasan

        agar boshqa mavzuda savol berishsa 'Uzr men bu mavzuda gaplasha olmayman

        seni javobing uzunligi har doim eng ko'p bilan 200 ta so'zdan iborat bo'lsin. Fagat mavzu bo'yicha berilgan savolga javob gaytar.
        savol: {message}

        Javob har doim oddiy text bo'lsin

    """

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=contents
    )
    return response.text

def index(request):
    return render(request, "index.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")
        
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index" "") 
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


def chat(request, agent_id):
    agents = Ai_agent.objects.all()
    user = request.user

    if agent_id != 0:
        agent = Ai_agent.objects.get(id=agent_id)
        history = History.objects.filter(agent_id=agent, user_id=user)

        return render(request, "chat.html", {"agent": agent, "agents": agents, "history": history})
    else:
        return render(request, "chat.html", {"agents": agents})


def ChatResponse(request, agent_id):
    if request.method == "POST":

        user = request.user
        ai_agent = Ai_agent.objects.get(id=agent_id)
        text = request.POST.get("text")
        ai_response = chat_agent(role=ai_agent.shaxsiyati, message=text)

        try:
            # AI javobini saqlash 
            new_agent_message = History.objects.create(
                user_id=user,
                agent_id=ai_agent,
                message=ai_response,
                sender="agent"
            )
            # User javobini saqlash
            new_user_message = History.objects.create(
                user_id=user,
                agent_id=ai_agent,
                message=text,
                sender="user"
            )
            print("User message saved:", new_user_message)
            print("AI response saved:", new_agent_message)
            return redirect("chat", agent_id)
        except Exception as e:
            messages.error(request, f"Xatolik: {e}")
            return redirect("chat", agent_id=agent_id)
