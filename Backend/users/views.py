from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages



class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, 'Your account has been created successfully! Please log in.')
            return redirect('login')  # Redirect to login page
        return render(request, 'users/signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your main page
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

def check_auth(request):
    return JsonResponse({'authenticated': request.user.is_authenticated})

# Add this function
def logout_view(request):
    logout(request)
    return redirect('login')


    #this code is before modifying

    