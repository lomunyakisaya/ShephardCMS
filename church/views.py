from enum import member
from urllib import request
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Sum, F, Q
from django.utils import timezone
from .models import Event, Leader, Member, Attendance, PrayerRequest, Announcement, Department, Notification, Service,  Income, Expense


# ----------------------
# Dashboard View
# ----------------------
@login_required
def dashboard(request):
    username = request.user.username
    # Announcements (published only)
    announcements = (Announcement.objects.filter(is_published=True).order_by('-date_posted')[:5])
    
    #Active members
    active_members = Member.objects.filter(membership_status='Active').count()
    
    #leaders
    leaders = Leader.objects.all().order_by('-date_started')
    
    #last five attendance records
    last_5_attendance = Attendance.objects.all().order_by('-timestamp')[:5]
    
    #departments
    departments = Department.objects.all()
       
    # Department notifications (global or user's department)
    notifications = (Notification.objects.filter(Q(department=request.user.department)).order_by('-created_at')[:5])

    # Upcoming events only
    upcoming_events = (Event.objects.filter(date__gte=timezone.now(),is_cancelled=False,is_published=True).order_by('date')[:5])

    # Public prayer requests (approved & not anonymous)
    prayer_requests = (PrayerRequest.objects.filter(is_anonymous=False,is_answered=True).order_by('-date_requested')[:5])
    #Last service total count for departments
    last_attendance = Attendance.objects.order_by('-timestamp').first()
    grant_total = last_attendance.last_attendance if last_attendance else 0
    context = {
        "active_members": active_members,
        "announcements": announcements,
        "notifications": notifications,
        "upcoming_events": upcoming_events,
        "prayer_requests": prayer_requests,
        "username" : username,
        "leaders": leaders,
        "departments": departments,
        "last_5_attendance": last_5_attendance,
        "last_attendance": last_attendance,
         "grant_total": grant_total,
    }
 
    return render(request, "church/dashboard.html", context)
#profile
@login_required
def profile_view(request):
    user = request.user
    member, created = Member.objects.get_or_create(user=user)

    if request.method == "POST":

        # Get form data
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        # -------- Basic Info Update --------
        if not first_name:
            messages.error(request, "First name cannot be empty.")
            return redirect("profile")

        if not email:
            messages.error(request, "Email cannot be empty.")
            return redirect("profile")

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        member.phone = phone

        user.save()
        member.save()

        # -------- Password Update (Optional) --------
        if old_password or new_password1 or new_password2:

            if not old_password:
                messages.error(request, "Enter your old password.")
                return redirect("profile")

            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
                return redirect("profile")

            if new_password1 != new_password2:
                messages.error(request, "New passwords do not match.")
                return redirect("profile")

            if len(new_password1) < 8:
                messages.error(request, "Password must be at least 8 characters.")
                return redirect("profile")

            user.set_password(new_password1)
            user.save()

            # Important: keeps user logged in
            update_session_auth_hash(request, user)

            messages.success(request, "Profile and password updated successfully.")
            return redirect("profile")

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "church/profile.html", {
        "member": member,
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
def finance_view(request):
   
    total_income = Income.objects.filter(status="Approved").aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Expense.objects.filter(status="Approved").aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expense

    context = {
        "income": total_income,
        "expense": total_expense,
        "balance": balance
    }
    return render(request,"church/finance.html",context)


#leader view
@login_required
def dept_leader_view(request):
    if not request.user.is_dept_leader:
        return redirect("permission_denied")
    return render(request, "church/dept_leader.html")
@login_required
def more_view(request):
    return render(request, "church/more.html")