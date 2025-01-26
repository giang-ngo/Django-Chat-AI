from django.shortcuts import render
from django.http import JsonResponse
import openai
from openai import OpenAI
import os
from openai import OpenAI

# Access https://platform.openai.com/api-keys to create an OpenAI API key.
# Access https://platform.openai.com/settings/organization/billing/overview to purchase credits.
client = OpenAI(api_key='input-your-key')  # input-your-key
# client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = chat_gpt(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')
