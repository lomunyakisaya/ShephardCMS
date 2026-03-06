# admin.py
from django.contrib import admin
from .models import Member, Department, Expense, ExpenseCategory, Income, IncomeCategory, Attendance, Event, Notification, PrayerRequest, Announcement,Leader, Service 

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
admin.site.register(Leader)
admin.site.register(Service)
admin.site.site_header = "MyChurch Admin"
admin.site.site_title = "MyChurch Admin Portal"
admin.site.index_title = "Welcome to MyChurch Admin Portal"
#admin.site.site_url = None Disable the "View Site" link in the admin header