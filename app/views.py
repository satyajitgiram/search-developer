from django.shortcuts import render, redirect
from .forms import ProjectForm, ReviewForm
from . import models
from .models import Tags
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects
from django.contrib import messages

# Create your views here.



def home(request):
    print("INSIDE HOME")
    project, search_query = searchProjects(request)
    custom_range, project = paginateProjects(request, project, 9)

    context = {'projects': project, 'search_query': search_query,'custom_range': custom_range}
    return render(request,"projects/index.html",context)

@login_required(login_url='login')
def addProject(request):
    profile  = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(" ",'').split(',')
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project =  form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tags.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('home')

    context = {'form':form}
    return render(request,"projects/project-form.html",context)


@login_required(login_url='login')
def editProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(" ",'').split(',')
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():

            project = form.save()
            for tag in newtags:
                tag, created = Tags.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('home')
    
    context = {'form':form, 'project':project}
    return render(request,"projects/project-form.html",context)


def singleProject(request,id):
    projectObj = models.Project.objects.get(id=id)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        # Update project vote count
        projectObj.getVoteCount
        
        messages.success(request,'your Review was successfully submitted!')
        return redirect('single_project', id=projectObj.id)


    context = {'project':projectObj, 'form':form}
    return render(request, 'projects/single_project.html',context)

def deleteProject(request,id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    
    if request.method == 'POST':
        project.delete()
        return redirect('home')


    context = {'object':project}
    return render(request, 'delete.html',context)
