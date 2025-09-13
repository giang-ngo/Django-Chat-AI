from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Chat, TrainingData


@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user).order_by('id')
    td = TrainingData.objects.filter(user=request.user).first()
    return render(request, "chatbot.html", {
        "chats": chats,
        "train_prompt": td.prompt if td else ""
    })


@login_required
@csrf_exempt
def train_bot(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt', '').strip()
        obj, _ = TrainingData.objects.get_or_create(user=request.user)
        obj.prompt = prompt
        obj.save()
        return JsonResponse({'status': 'ok', 'message': 'Prompt lưu thành công'})

    td = TrainingData.objects.filter(user=request.user).first()
    return JsonResponse({'prompt': td.prompt if td else ''})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('chatbot')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('chatbot')
        return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('chatbot')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password', '').strip()
        password2 = request.POST.get('confirm_password', '').strip()

        if password1 != password2:
            return render(request, 'register.html', {'error_message': "Passwords don't match"})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': "Username already exists"})

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password1)
            auth_login(request, user)
            return redirect('chatbot')
        except Exception as e:
            return render(request, 'register.html', {'error_message': f"Error creating account: {e}"})

    return render(request, 'register.html')


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login_view')
