from django.contrib import admin
from .models import UserProfile, Ai_agent, History
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Ai_agent)
admin.site.register(History)