from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, PasswordChangeForm

from .models import User, Profile

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_password(self, password):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(password)
        return password


class LoginForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'password')

class UpdateProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Profile
        fields = ('firstName', 'lastName') 

class ChangePasswordForm(PasswordChangeForm):
    username = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username')
