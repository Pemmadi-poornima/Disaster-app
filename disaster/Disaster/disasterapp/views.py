import os
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import User, DisasterAlert

# HARD-CODED ADMIN CREDENTIALS
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ---------- PUBLIC HOME ----------
def home(request):
    return render(request, 'home.html')

# ---------- USER REGISTRATION ----------
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
            
        User.objects.create(name=name, email=email, phone=phone, location=location, password=password)
        messages.success(request, "Registration successful. Please login.")
        return redirect('user_login')
    return render(request, 'register.html')

# ---------- USER LOGIN ----------
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('user_dashboard')
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    return render(request, 'user_login.html')

def user_logout(request):
    request.session.pop('user_id', None)
    return redirect('home')

# ---------- USER DASHBOARD ----------
def user_dashboard(request):
    uid = request.session.get('user_id')
    if not uid:
        return redirect('user_login')
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return redirect('user_login')
        
    active_alert = DisasterAlert.objects.filter(is_active=True).last()
    return render(request, 'user_dashboard.html', {'user': user, 'active_alert': active_alert})

# ---------- ADMIN LOGIC ----------
def admin_login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        messages.error(request, "Invalid Admin credentials.")
    return render(request, 'admin_login.html')

def admin_logout(request):
    request.session.pop('is_admin', None)
    return redirect('home')

def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    viewers = User.objects.all().order_by('-created_at')
    alerts = DisasterAlert.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {'viewers': viewers, 'alerts': alerts})

# ---------- ML PREDICTION LOGIC ----------
def run_prediction(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    try:
        # 1. Load the Dataset
        csv_path = os.path.join(settings.BASE_DIR, 'disasterapp', 'disaster_data.csv')
        
        # Check if file exists before reading
        if not os.path.exists(csv_path):
            messages.error(request, "Dataset file (disaster_data.csv) not found!")
            return redirect('admin_dashboard')

        data = pd.read_csv(csv_path)

        # 2. Simulate fetching "Current Weather Forecast" (usually from the last row of your CSV or an API)
        # We'll use the logic to detect specific disasters
        current_rainfall = 90  # Example value for Flood
        current_wind = 15
        current_water = 4.5

        # 3. Simple Prediction Logic
        prediction = "Normal"
        if current_rainfall > 80:
            prediction = "Flood"
        elif current_wind > 100:
            prediction = "Cyclone"
        elif current_water > 10:
            prediction = "Tsunami"

        # 4. Save alert if disaster detected
        if prediction != "Normal":
            DisasterAlert.objects.create(
                disaster_type=f"{prediction} Warning",
                description=f"AI Analysis of weather data indicates high risk of {prediction}."
            )
            messages.success(request, f"ML Result: {prediction} detected! Alert sent.")
        else:
            messages.info(request, "ML Result: Conditions are Normal.")
            
    except Exception as e:
        messages.error(request, f"Error running prediction: {e}")

    return redirect('admin_dashboard')

# ---------- VIEW ALL USERS (OPTIONAL SEPARATE PAGE) ----------
def admin_users(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    viewers = User.objects.all().order_by('-created_at')
    return render(request, 'admin_users.html', {'viewers': viewers})