from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser): 
    phone = models.CharField(max_length=15, unique=False, null=True, blank=True)
    is_pastor = models.BooleanField(default=False)
    is_church_admin = models.BooleanField(default=False)
    is_treasurer = models.BooleanField(default=False)
    is_dept_leader = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username

class Leader(models.Model):
    name=models.ForeignKey('Member', on_delete=models.CASCADE)
    department=models.ForeignKey('Department', on_delete=models.CASCADE, related_name='leaders')
    date_started = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.name} - {self.department}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
      return self.name

class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=False, blank=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    baptised = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False, null=False, blank=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    membership_status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Suspended', 'Suspended'),
            ('Inactive', 'Inactive')
        ],
        default='Active'
    )

    is_married = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(Member, on_delete=models.PROTECT, null=False, related_name='added_expenses', )
    approved_by = models.ForeignKey(Member, on_delete=models.PROTECT, null=True, related_name='approved_expenses')

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.name} - {self.amount}"

class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='approved_incomes')

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey('Member', on_delete=models.CASCADE, null=False, blank=False)
    is_cancelled = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name} ({self.date.date()}) - {'Published' if self.is_published else 'Unpublished'}"

 
class Service(models.Model):
    name = models.CharField(choices=[
        ('Sunday Service', 'Sunday Service'),
        ('Midweek Service', 'Midweek Service'),
        ('Special Service', 'Special Service'),
        ('Other', 'Other')
    ], max_length=100)
    date = models.DateTimeField(null=False, blank=False)
    description = models.TextField(blank=True)
    programmed_by = models.ForeignKey('Member', on_delete=models.CASCADE, null=False, related_name='programmed_services')
    organizer = models.ForeignKey('Member', on_delete=models.CASCADE, null=False, related_name='organized_services')

    def __str__(self):
        return f"{self.name} ({self.date.date()})"   
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey('Member', on_delete=models.CASCADE, null=False)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title   
class PrayerRequest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    requested_by = models.CharField(max_length=1000, blank=False, null=False)
    is_answered = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    # Notifications / Announcements
class Notification(models.Model):  
        title = models.CharField(max_length=200, blank=False, null=False)
        content = models.TextField(blank=False, null=False)
        posted_by = models.ForeignKey('Member', on_delete=models.CASCADE, null=False)
        created_at = models.DateTimeField(auto_now_add=True)
        department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
           
    
        def __str__(self):
            return f"Notification for {self.title} at {self.created_at}"
        
        
class Suggestion(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Attendance(models.Model):
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    male_count = models.PositiveIntegerField(default=0)
    female_count = models.PositiveIntegerField(default=0)
    child_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.service_type}"
    @property
    def total_attendance(self):
        return self.male_count + self.female_count + self.child_count

