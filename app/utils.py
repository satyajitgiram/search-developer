from django.db.models import Q
from app.models import Project, Tags
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage    


def paginateProjects(request, project, results):
    page = request.GET.get('page')
    results = results
    paginator = Paginator(project, results)

    try:
        project = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        project = paginator.page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        project = paginator.page(page)

    leftIndex = (int(page) -1)

    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) +3)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1 
    
    custom_range = range (leftIndex, rightIndex)
    
    return custom_range, project


def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tags.objects.filter(name__icontains=search_query)

    project = Project.objects.distinct().filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(owner__name__icontains=search_query) | Q(tags__in = tags))

    return project, search_query