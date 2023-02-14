from django.shortcuts import render, redirect
from .forms import ProjectForm
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    project = models.Project.objects.all()
    context = {'projects': project}
    return render(request,"projects/index.html",context)

@login_required(login_url='login')
def addProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,"projects/project-form.html",context)


@login_required(login_url='login')
def editProject(request, id):
    project = models.Project.objects.get(id=id)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,"edit_project.html",context)

def singleProject(request,id):
    project = models.Project.objects.get(id=id)
    context = {'project':project}
    return render(request, 'projects/single_project.html',context)

def deleteProject(request,id):
    project = models.Project.objects.get(id=id)
    
    if request.method == 'POST':
        project.delete()
        return redirect('home')


    context = {'project':project}
    return render(request, 'delete_project.html',context)
