from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.db.models import Sum
from django.utils import timezone
from .models import Event, Member, Attendance, PrayerRequest, Announcement, Department, Notification
from .forms import CustomUserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm

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
    return render(request, "church/home.html")


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


# ----------------------
# Dashboard View
# ----------------------
@login_required
def dashboard(request):
    member = getattr(request.user, "member", None)

    # Upcoming events (next 5)
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by("date")[:5]

    # Leaders
    leaders = Member.objects.filter(is_leader=True).select_related("department")

    # Announcements
    announcements = Announcement.objects.all().order_by("-date_posted")[:5]

    # Active members count
    active_members = Member.objects.filter(membership_status="Active").count()

    # Last 5 attendance
    last_5_attendance = Attendance.objects.select_related("member", "event").order_by("-timestamp")[:5]

    # Latest 5 prayer requests
    prayer_requests = PrayerRequest.objects.filter(is_anonymous=False).order_by("-date_requested")[:5]

    # Total attendance
    totals = Attendance.objects.aggregate(
        total_male=Sum("male_count"),
        total_female=Sum("female_count"),
        total_children=Sum("child_count")
    )
    total_attendance = (totals["total_male"] or 0) + (totals["total_female"] or 0) + (totals["total_children"] or 0)

    context = {
        "member": member,
        "profile_pic": member.profile_pic.url if member and member.profile_pic else None,
        "upcoming_events": upcoming_events,
        "leaders": leaders,
        "active_members": active_members,
        "departments": Department.objects.all(),
        "last_5_attendance": last_5_attendance,
        "total_attendance": total_attendance,
        "prayer_requests": prayer_requests,
        "announcements": announcements,
    }

    return render(request, "church/dashboard.html", context)


# ----------------------
# Main View (Prayer + Notifications)
# ----------------------
@login_required
def main_view(request):
    member = getattr(request.user, "member", None)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        is_anonymous = request.POST.get("is_anonymous") == "on"

        if not title or not content:
            messages.error(request, "Both title and content are required.")
        else:
            PrayerRequest.objects.create(
                requested_by=request.user.username,
                title=title,
                description=content,
                is_anonymous=is_anonymous
            )
            messages.success(request, "Prayer request submitted successfully.")
        return redirect("main")

    user_prayers = PrayerRequest.objects.filter(requested_by=request.user.username).order_by("-date_requested")
    notifications = Notification.objects.filter(posted_by=member).order_by("-created_at") if member else []

    return render(request, "church/main.html", {
        "user_prayers": user_prayers,
        "notifications": notifications,
        "member": member
    })


# ----------------------
# Leader Panel View
# ----------------------
@login_required
def leader_view(request):
    member = getattr(request.user, "member", None)
    if not member or not member.is_leader:
        return HttpResponseForbidden("You do not have permission to access this page.")

    department = member.department
    department_members = Member.objects.filter(department=department)

    return render(request, "church/leader.html", {
        "department": department,
        "department_members": department_members
    })


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