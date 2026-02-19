from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    leader = models.ForeignKey('Member', on_delete=models.PROTECT, null=False, blank=False, related_name='department_leader')

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField()
    date_joined = models.DateField(auto_now_add=True)
    baptised = models.BooleanField(default=False)

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
    added_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='approved_expenses')

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
    added_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)

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
