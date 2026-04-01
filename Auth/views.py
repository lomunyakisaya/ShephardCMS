
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#******************************************************
#SIGNUP_VIEW
#******************************************************

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        #if not all fields
        if not all([username, email, password, password2]):
            messages.error(request, "All fields are required")
            return redirect( 'register' )
        #if username or email exist 
        if CustomUser.objects.filter(username=username, email=email).exists():
            messages.error(request, "Username or Email already exist")
            return redirect('register')
        #if passwords do not match
        if password != password2:
            messages.error(request, "Password do not match")
            return redirect('register')
        #then create user
        user = CustomUser.objects.create_user(username=username,password=password, email=email)
        messages.success(request, "Account Created Successfully")
        return redirect('login')
    return render(request, 'auth/signup.html')
#******************************************************
#LOGIN
#******************************************************
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect('login')
    return render(request, "auth/login.html")
#******************************************************
#LOGOUT
#******************************************************
def logout_view(request):
    logout(request)
    return redirect("login")
#******************************************************
#HOME
#******************************************************
#def home_view(request):
 #   return render(request, "auth/home.html")
#******************************************************
#END
#******************************************************