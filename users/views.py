from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Profile, Message
from .models import Skill
from app.models import Project
from .utils import searchProfiles
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User with this id doesn't exist ")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, "Logged in ")
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profile')
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
            return redirect('edit-account')

        else:
            messages.error(request,"An error occured during account registation")


    
    context = {'page': page,'form':form}
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    messages.info(request, "User logout successfully")

    logout(request)
    return redirect('login')


def profile(request):
    profiles, search_query = searchProfiles(request)
    context = {'profiles':profiles, 'search_query':search_query}
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

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Updated Successfully!")
            return redirect('account')



    context = {'form':form}
    return render(request, 'users/profile_form.html', context)
    

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill Added Successfully!")
            return redirect('account')


    context={'form':form}   
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request,"Skill Updated Successfully!")
            return redirect('account')


    context={'form':form}   
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def delete_skill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request,"Skill Deleted Successfully!")
        return redirect('account')


    context = {'object':skill}
    return render(request, 'delete.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request, 'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context={'message':message}
    return render(request, 'users/message.html',context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)

    context = {'recipient':recipient}
    return render(request,'users/message_form.html',context)