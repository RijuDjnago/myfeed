from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(required=False)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'bio', 'profile_image', 'dob']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'bio', 'profile_image', 'dob']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }







