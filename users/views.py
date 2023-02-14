from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from app.models import Project
from .forms import CustomUserCreationForm

# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User with this id doesn't exist ")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.error(request, "Logged in ")
            print("Logged in ")
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Username or password is incorrect")


    return render(request, 'users/login_register.html')

def registerUser(request): 

    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,"User Account created successfully")
            login(request, user)
            return redirect('profiles')

        else:
            messages.error(request,"An error occured during account registation")


    
    context = {'page': page,'form':form}
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    messages.info(request, "User logout successfully")

    logout(request)
    return redirect('login')


def profile(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html',context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description = "")
    context = {'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile=request.user.profile
    skills = profile.skill_set.all()
    allproj = profile.project_set.all()

    context={'profile':profile,
    'skills':skills,
    'allproj':allproj
    }
    return render(request, 'users/account.html',context)

    