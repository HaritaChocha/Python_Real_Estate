from django.contrib import admin
from django.contrib.auth import get_user_model

# Local Import
from .models import Profile

# User Model
User = get_user_model()

# Site Registration
admin.site.register(User)
admin.site.register(Profile)