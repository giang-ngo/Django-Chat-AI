from django.apps import AppConfig
import sys


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'

    def ready(self):
        print("[DEBUG] ChatbotConfig.ready() called",
              flush=True, file=sys.stderr)