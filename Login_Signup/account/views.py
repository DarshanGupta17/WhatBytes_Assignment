from django.shortcuts import render,HttpResponse , redirect
from account.forms import SignUpForm,LoginForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm , PasswordResetForm
from django.contrib.auth.decorators import login_required
from .models import Profile
import datetime
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

User_model = get_user_model()
# Create your views here.

# to send the reset link only to the user that exist in database
class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No user is associated with this email address.")
        return email

class Password_Reset_View(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'passwordReset/passwordReset.html'
    email_template_name = 'email.html'
    success_url = reverse_lazy('password_reset_done')

class Password_Reset_Done_View(auth_views.PasswordResetDoneView):
    template_name = 'passwordReset/passwordResetDone.html'

class Password_Reset_Confirm_View(auth_views.PasswordResetConfirmView):
    template_name = 'passwordReset/passwordResetConfirm.html'
    success_url = reverse_lazy('password_reset_complete')

class Password_Reset_Complete_View(auth_views.PasswordResetCompleteView):
    template_name = 'passwordReset/passwordResetComplete.html'

def Login(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = None

            user = authenticate(username=username, password=password)

            if user is None:
                try:
                    user_model = get_user_model()
                    user_instance = user_model.objects.get(email=username)
                    user = authenticate(username=user_instance.username, password=password)
                except user_model.DoesNotExist:
                    user = None

            if user is None:
                messages.error(request, "Invalid email or password")
                return redirect('login')

            messages.success(request, "Logged in successfully")
            
            # profile is to show when user was last active 
            profile = Profile.objects.get(user = user)
            profile.last_active = datetime.date.today()
            profile.save() 
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})

def Register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User Created Successfully")
            profile = Profile()
            profile.user = user
            profile.last_active = datetime.date.today()
            profile.save()
            return redirect("login")
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
    else:
        form = SignUpForm()
    return render(request,'register.html',{'form':form})
            
@login_required(login_url="login")
def Home(request):
    return render(request , 'home.html')

@login_required(login_url="login")
def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect('home')  # Redirect to a profile page or another page of your choice
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'changePassword.html', {'form': form})


def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def show_profile(request):
    profile = Profile.objects.get(user = request.user)

    return render(request,'Profile.html',{'profile':profile})