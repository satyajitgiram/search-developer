from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from app.models import Project, Review


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )
    review.value = data['value']
    review.body = data.get('body',"")
    review.save()
    project.getVoteCount

    print('DATA',data)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
