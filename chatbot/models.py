import json
from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    topics = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_topics(self, topics_list):
        self.topics = json.dumps(topics_list or [])

    def get_topics(self):
        if self.topics:
            return json.loads(self.topics)
        return []

    def __str__(self):
        return f"Chat {self.id} - {self.user.username}"


class TrainingData(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    prompt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prompt {self.user.username} - {self.prompt[:30]}..."
