from urllib import request

from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models import Q
from django.utils import timezone
from .models import Event, Leader, Member, Attendance, PrayerRequest, Announcement, Department, Notification, Service


User = get_user_model()

# ----------------------
# Authentication Views
# ----------------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "church/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "church/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        user.phone = phone
        user.save()

        auth_login(request, user)
        return redirect("dashboard")

    return render(request, "church/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "church/login.html")


def logout_view(request):
    auth_logout(request)
    return redirect("home")


def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by("date")[:5]
    context = {
        "upcoming_events": upcoming_events
    }
    return render(request, "church/home.html", context)

#Access Denied View
def permission_denied_view(request):
    return render(request, "church/403.html", status=403)


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


# ----------------------
# Dashboard View
# ----------------------
@login_required
def dashboard(request):
    username = request.user.username
    # Announcements (published only)
    announcements = (Announcement.objects.filter(is_published=True).order_by('-date_posted')[:5])

    # Department notifications (global or user's department)
    notifications = (Notification.objects.filter(Q(department=request.user.department)).order_by('-created_at')[:5])

    # Upcoming events only
    upcoming_events = (Event.objects.filter(date__gte=timezone.now(),is_cancelled=False,is_published=True).order_by('date')[:5])

    # Public prayer requests (approved & not anonymous)
    prayer_requests = (PrayerRequest.objects.filter(is_anonymous=False,is_answered=True).order_by('-date_requested')[:5])


    context = {
        "announcements": announcements,
        "notifications": notifications,
        "upcoming_events": upcoming_events,
        "prayer_requests": prayer_requests,
        "username" : username,
    }

    return render(request, "church/dashboard.html", context)
# ----------------------
# Me View (Prayer + Notifications)
# ----------------------
@login_required
def me_view(request):
    return render(request, "church/me.html",)


# ----------------------
# Profile Edit View
# ----------------------
@login_required
def profile_edit_view(request):
    user = request.user
    member, _ = Member.objects.get_or_create(user=user)

    if request.method == "POST":

        # --- Update Email & Phone ---
        if "update_contact" in request.POST:
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()

            if not email:
                messages.error(request, "Email cannot be empty.")
            else:
                user.email = email
                member.phone = phone
                user.save()
                member.save()
                messages.success(request, "Contact info updated successfully.")
            return redirect("edit_profile")

        # --- Update Profile Picture ---
        elif "update_profile_pic" in request.POST:
            profile_pic = request.FILES.get("profile_pic")
            if profile_pic:
                member.profile_pic = profile_pic
                member.save()
                messages.success(request, "Profile picture updated successfully.")
            else:
                messages.error(request, "Please select a picture to upload.")
            return redirect("edit_profile")

        # --- Change Password ---
        elif "change_password" in request.POST:
            old_password = request.POST.get("old_password")
            new_password1 = request.POST.get("new_password1")
            new_password2 = request.POST.get("new_password2")

            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
            elif new_password1 != new_password2:
                messages.error(request, "New passwords do not match.")
            elif len(new_password1) < 8:
                messages.error(request, "New password must be at least 8 characters.")
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
            return redirect("edit_profile")

    # GET request
    return render(request, "church/profile.html", {
        "user": user,
        "member": member,
        "profile_pic": member.profile_pic.url if member and member.profile_pic else None
    })
    
# Admin view 
@login_required
def admin(request):
    if not request.user.is_admin:
        return redirect("permission_denied")
    return render(request, "church/admin.html")

#pastor view
@login_required
def pastor_view(request):
    if not request.user.is_pastor:
        return redirect("permission_denied")
    return render(request, "church/pastor.html")


#church admin view
@login_required
def church_admin_view(request):
    if not request.user.is_church_admin:
        return redirect("permission_denied")
    return render(request, "church/church_admin.html")


#treasurer view
@login_required
def treasurer_view(request):
    if not request.user.is_treasurer:
        return redirect("permission_denied")
    return render(request, "church/treasurer.html")


#leader view
@login_required
def dept_leader_view(request):
    if not request.user.is_dept_leader:
        return redirect("permission_denied")
    return render(request, "church/dept_leader.html")
