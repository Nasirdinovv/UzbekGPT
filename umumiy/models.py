from django.db import models
from django.conf import settings














class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode = models.CharField(max_length=50)  # Matematika, Tarix, va h.k.
    title = models.CharField(max_length=255) # Suhbat mavzusi (tarix uchun)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_bot = models.BooleanField(default=False)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)