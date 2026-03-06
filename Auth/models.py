from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser): 
    phone = models.CharField(max_length=15, unique=False, null=True, blank=True)
    is_pastor = models.BooleanField(default=False)
    is_church_admin = models.BooleanField(default=False)
    is_treasurer = models.BooleanField(default=False)
    is_dept_leader = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    department = models.ForeignKey('church.Department', on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.username
