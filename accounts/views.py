from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail

# Local Imports
from .forms import RegisterForm, LoginForm, UpdateProfileForm, ChangePasswordForm
from .models import Profile

User = get_user_model()

# Helper Function
def mailer(message, reciever=None):
    subject = "New Django App Registration"

    send_mail(
                subject=subject,
                message=message,
                from_email='tarang.chikhalia@yahoo.com',
                fail_silently=False,
                recipient_list= reciever or ['tarang.chikhalia@yahoo.com']
            )

def passwordHelper(request):
    pass

# Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.clean_username()
            email = form.clean_email()
            password = form.clean_password('newUser@123')
            user = form.save()
            print(form)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            print(user)
            # Create Profile
            profile = Profile(user=user, firstName=first_name, lastName=last_name)
            profile.save()
            
            message_to_admin = 'A new user {} with email- {} has asked for registration. Please Register the new user from the Admin Console'.format(username, email)
            mailer(message_to_admin)

            print('Mail Sent to Admin')
            return render(request,'accounts/afterRegistration.html')
        else:
            print('Error')
    else:
        form = RegisterForm()

    context ={
        'form':form,
        'source': 'Registration',
    }

    return render(request, 'accounts/form.html', context)

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('eproperty:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/form.html', {
        'form': form,
        'source': 'Change Password'
    })

def firstLoginPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['old_password']
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        login(request, user)
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('eproperty:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/form.html', {
        'form': form,
        'source': 'Change Password'
    })

@csrf_protect
def loginUser(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.first_login:
                    print("Here first login = false")
                    user.first_login = False
                    user.save()
                    print("User saved")
                    print("redirecting to change password")
                    return redirect('accounts:firstLoginPassword')
                    # form = passwordHelper(request)
                    # return render(request, 'accounts/form.html', {
                    #     'form': form,
                    #     'source': 'Login'
                    # })
                login(request, user)
                return redirect('eproperty:home')
        else:
            return render(request, 'accounts/login.html', {
                'message': 'Login failed. Please check your username and password.'
            })
    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('eproperty:home')

@login_required
def updateProfile(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        instance = get_object_or_404(Profile, user=user)
        form = UpdateProfileForm(request.POST, instance=instance)
        if form.is_valid():
            profile = form.save(commit=False)
            user = User.objects.get(username=username)
            # print(user)
            profile.user = user
            profile.save()
            messages.success(request, 'Your Profile was successfully updated!')
            return redirect('eproperty:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user = get_object_or_404(User, username=username)
        instance = get_object_or_404(Profile, user=user)
        form = UpdateProfileForm(instance=instance)
    return render(request, 'accounts/form.html', {
        'source': 'Update Profile',
        'form': form
    })

@login_required
def ViewProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    print(profile)

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def activation(request):
    user = request.user
    if user.is_admin:
        user_list = User.objects.filter(active=False)
        context = {
            'user_list': user_list
        } 
        return render(request, 'accounts/activation.html', context)
    else:
        print("Error")
        return redirect('eproperty:home')

@login_required
def activateUser(request, username):
    if request.user.is_admin:
        user = get_object_or_404(User, username=username)
        user.active = True
        user.save()

        #temp password
        pswd = "newUser@123"

        # Send Mail
        message = "Your account has been activated by the administrator. Your Temperory password: {}. Please reset your password on first use.".format(pswd)
        mailer(message, [user.email])

        print('mail sent to user')
        return redirect('accounts:activation')
    else:
        print('error')
        return redirect('eproperty:home')