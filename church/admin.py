# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Member, Department, Expense, ExpenseCategory, Income, IncomeCategory, Attendance, Event, Notification, PrayerRequest, Announcement

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active',)

admin.site.register(Member)
admin.site.register(Department)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Income)
admin.site.register(IncomeCategory)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(PrayerRequest)
admin.site.register(Announcement)

