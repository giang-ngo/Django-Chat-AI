from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from openai import OpenAI
import os
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

# Access https://platform.openai.com/api-keys to create an OpenAI API key.
# Access https://platform.openai.com/settings/organization/billing/overview to purchase credits.
# Please get your OpenAI API key to use ChatGPT's services.
client = OpenAI(api_key='YOUR-API-KEY-HERE')  # input-your-key
# client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def chat_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: Unable to process your request. {str(e)}"


def chatbot(request):
    # chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = chat_gpt(message)
        if request.user.is_authenticated:
            chat = Chat(user=request.user, message=message,
                        response=response, created_at=timezone.now())
            chat.save()
        return JsonResponse({'message': message, 'response': response})
    chats = Chat.objects.filter(
        user=request.user) if request.user.is_authenticated else []
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        if password1 == password2:
            try:
                user = User.objects.create_user(
                    username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password don\'t match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('chatbot')
