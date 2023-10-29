from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from app.models import Project


@api_view(['GET','POST'])
def getRoutes(request):
    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/1'},
        {'POST':'api/projects'},
        {'PUT':'api/projects/1'},
        {'DELETE':'api/projects/1'}
    ]

    return Response(routes)    


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def getProject(request,pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)
