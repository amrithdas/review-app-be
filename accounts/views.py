import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import SignUpForm, LoginForm
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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