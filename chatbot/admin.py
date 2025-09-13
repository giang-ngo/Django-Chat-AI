from django.contrib import admin
from django.utils.html import format_html
from .models import Chat, TrainingData


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "short_message",
                    "short_response", "short_topics", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("message", "response", "user__username", "topics")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "full_message",
                       "full_response", "full_topics")
    fieldsets = (
        (None, {
            "fields": ("user", "full_message", "full_response", "full_topics", "created_at")
        }),
    )

    def user_link(self, obj):
        return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', obj.user.id, obj.user.username)
    user_link.short_description = "User"


    def short_message(self, obj):
        return (obj.message[:60] + "...") if len(obj.message) > 60 else obj.message
    short_message.short_description = "Message"

    def full_message(self, obj):
        return format_html('<textarea style="width:100%;height:60px;" readonly>{}</textarea>', obj.message)
    full_message.short_description = "Full Message"


    def short_response(self, obj):
        return (obj.response[:60] + "...") if len(obj.response) > 60 else obj.response
    short_response.short_description = "Response"

    def full_response(self, obj):
        return format_html('<textarea style="width:100%;height:60px;" readonly>{}</textarea>', obj.response)
    full_response.short_description = "Full Response"

    def short_topics(self, obj):
        return ", ".join(obj.topics) if obj.topics else "-"
    short_topics.short_description = "Topics"

    def full_topics(self, obj):
        return format_html('<textarea style="width:100%;height:40px;" readonly>{}</textarea>', ", ".join(obj.topics) if obj.topics else "")
    full_topics.short_description = "Full Topics"

@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "short_prompt",
                    "created_at", "updated_at")
    search_fields = ("prompt", "user__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "full_prompt")
    fieldsets = (
        (None, {
            "fields": ("user", "full_prompt", "created_at", "updated_at")
        }),
    )

    def user_link(self, obj):
        if obj.user:
            return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', obj.user.id, obj.user.username)
        return "-"
    user_link.short_description = "User"

    def short_prompt(self, obj):
        return (obj.prompt[:60] + "...") if len(obj.prompt) > 60 else obj.prompt
    short_prompt.short_description = "Prompt"

    def full_prompt(self, obj):
        return format_html('<textarea style="width:100%;height:100px;" readonly>{}</textarea>', obj.prompt)
    full_prompt.short_description = "Full Prompt"
