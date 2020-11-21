from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from view.models import ViewUser
from .serializers import ViewUserSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def viewuser_list(request):
    if request.method == 'GET':
        users=ViewUser.objects.all()
        serializers=ViewUserSerializer(users,many=True)
        return Response(serializers.data)
    #elif request.method == 'POST':
    '''
        data=JSONParser().parse(request)
        serializers=ViewUserSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)
            '''
@api_view(['PUT'])
def viewuser_Update(request,id):
    try:
        user=ViewUser.objects.get(id=id)
    except ViewUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializers=ViewUserSerializer(user,data=request.data)
        data={}
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
