from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from django.utils import timezone


openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    print(request.user,"88888888888888888888888888888888888888888")
    if request.user.username == "":
        return redirect("login")
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

# %%%%%%%%%%%%%%%%%%%needs to be change%%%%%%%%%%%%%%%%%%
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

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 == password2:
#             try:
#                 user = User.objects.create_user(username, email, password1)
#                 user.save()
#                 auth.login(request, user)
#                 return redirect('chatbot')
#             except:
#                 error_message = 'Error creating account'
#                 return render(request, 'register.html', {'error_message': error_message})
#         else:
#             error_message = 'Password dont match'
#             return render(request, 'register.html', {'error_message': error_message})
#     return render(request, 'register.html')

def is_alphanumeric(value):
    has_letter = any(char.isalpha() for char in value)
    has_digit = any(char.isdigit() for char in value)
    return has_letter and has_digit

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validate username (alphanumeric)
        if not is_alphanumeric(username):
            error_message = 'Username must be alphanumeric'
            return render(request, 'register.html', {'error_message': error_message})

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            error_message = 'Invalid email format'
            return render(request, 'register.html', {'error_message': error_message})

        # Validate password
        try:
            validate_password(password1)
        except ValidationError as e:
            error_message = ', '.join(e.messages)
            return render(request, 'register.html', {'error_message': error_message})

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'This Username already Registered'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})
    
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
