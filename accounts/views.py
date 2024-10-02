import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import SignUpForm, LoginForm
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = SignUpForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Signup successful'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@ensure_csrf_cookie
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON input'}, status=400)

        form = LoginForm(data)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authentication successful")
                login(request, user)
                url = reverse('home')
                # response = JsonResponse({'redirect_url': url})
                # response.set_cookie('csrftoken', get_token(request))
                return JsonResponse({'Success': 'Logged In'}, status=200)
            else:
                print("Authentication failed")
                return JsonResponse({'error': 'Invalid username or password'}, status=401)
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def check_auth(request):
    return JsonResponse({'isAuthenticated': True})

def check_auth_status(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'isAuthenticated': is_authenticated})

def user_logout(request):
    logout(request)
    response = JsonResponse({'message': 'Logged out successfully'}, status=200)
    response.delete_cookie('sessionid')  # Ensure sessionid cookie is deleted
    return response

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_token = data.get('id_token')

        # Verify the ID token
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        user_info = response.json()
        email = user_info.get('email')
        
        User = get_user_model()

        # Here, change the 'username' to 'email' to match your USERNAME_FIELD
        user, created = User.objects.get_or_create(email=email, defaults={'name': user_info.get('name')})

        # Log the user in
        login(request, user)
        
        return JsonResponse({'Success': 'Logged In'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    data = {
        'name': user.name,
        'pincode': user.pincode,
        'bio': user.bio,
    }
    return Response(data)