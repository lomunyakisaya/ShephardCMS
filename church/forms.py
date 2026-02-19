# church/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Member
User= get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone')  # include your phone field
        
class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    profile_picture = forms.ImageField(required=False)
    
class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Member
        fields = ["phone", "profile_pic"]

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class CustomPasswordChangeForm(PasswordChangeForm):
    # This inherits from Django’s PasswordChangeForm
    pass