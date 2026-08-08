from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('pastor', 'Pastor'),
        ('church_admin', 'Church Admin'),
        ('treasurer', 'Treasurer'),
        ('dept_leader', 'Department Leader'),
        ('admin', 'Admin'),
    ]

    phone = models.CharField(max_length=15, unique=False, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    baptised = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    department = models.ForeignKey('church.Department', on_delete=models.SET_NULL, null=True, blank=True)
    membership_status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('Suspended', 'Suspended'), ('Inactive', 'Inactive')],
        default='Active',
    )
    is_married = models.BooleanField(default=False)
    date_joined = models.DateField(default=date.today)

    is_pastor = models.BooleanField(default=False)
    is_church_admin = models.BooleanField(default=False)
    is_treasurer = models.BooleanField(default=False)
    is_dept_leader = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def sync_role_flags(self):
        self.is_pastor = self.role == 'pastor'
        self.is_church_admin = self.role == 'church_admin'
        self.is_treasurer = self.role == 'treasurer'
        self.is_dept_leader = self.role == 'dept_leader'
        self.is_admin = self.role == 'admin'
        return self

    def assign_role(self, role):
        if role not in dict(self.ROLE_CHOICES):
            raise ValueError(f'Unsupported role: {role}')
        self.role = role
        self.sync_role_flags()
        return self

    def save(self, *args, **kwargs):
        self.sync_role_flags()
        return super().save(*args, **kwargs)

    @property
    def member(self):
        return self

    def __str__(self):
        return self.username or self.email or f'User {self.pk}'
