import json
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatSession, ChatMessage

@login_required(login_url='/admin/login/')
def chat_view(request):
    sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chat.html', {'sessions': sessions})

@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get('message')
        mode = data.get('mode', 'Suhbat')
        
        session, _ = ChatSession.objects.get_or_create(
            user=request.user, mode=mode,
            defaults={'title': user_msg[:30]}
        )
        ChatMessage.objects.create(session=session, text=user_msg, is_bot=False)

        # AI-ga qat'iy yo'riqnoma berish
        prompts = {
            "Matematika": "Sen faqat matematika o'qituvchisisan. Savollarga faqat matematik formula va mantiq bilan javob ber. Agar foydalanuvchi boshqa mavzuda gapirsa, xushmuomalalik bilan rad et.",
            "Tarix": "Sen professional tarixchisan. Faqat tarixiy voqealar haqida gapir.",
            "Suhbat": "Sen aqlli yordamchisan, xohlagan mavzuda suhbatlash."
        }
        
        try:
            genai.configure(api_key="AIzaSyD8A1zXJAjUTC-KJSKfJC2dY8an0lf0Egg") 
            model = genai.GenerativeModel('gemini-1.5-flash')
            full_prompt = f"{prompts.get(mode, '')} \nFoydalanuvchi: {user_msg}"
            response = model.generate_content(full_prompt)
            
            bot_reply = response.text
            ChatMessage.objects.create(session=session, text=bot_reply, is_bot=True)
            return JsonResponse({'reply': bot_reply, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'reply': f"Xato: {str(e)}", 'status': 'error'})

# Tarixni yuklash uchun yangi View
@login_required
def get_session_messages(request, session_id):
    session = ChatSession.objects.get(id=session_id, user=request.user)
    messages = session.messages.all().order_by('timestamp')
    data = [{'text': m.text, 'is_bot': m.is_bot} for m in messages]
    return JsonResponse({'messages': data, 'mode': session.mode})


