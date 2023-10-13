from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def get_default_creator():
    User = get_user_model()
    user = User.objects.first()
    if user:
        return user.id
    return None


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    participants = models.ManyToManyField(User, related_name='group_chats')
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='group_chat_creator', editable=False, default=get_default_creator)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.creator:
            self.creator = get_default_creator()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}-{self.id}"

    
class Message(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.body
