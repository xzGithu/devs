from rest_framework import serializers,viewsets,routers
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from models import History_uint,History_text, History_str,History


class UintSerializer(serializers.ModelSerializer):
    class Meta:
        model = History_uint
        fields = '__all__'
class StrSerializer(serializers.ModelSerializer):
    class Meta:
        model = History_str
        fields = '__all__'

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = History_text
        fields = '__all__'
class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields= ('url', 'username', 'email', 'is_staff')
class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ('url', 'username', 'email', 'is_staff')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Stanrdsetpag(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None
class MyPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"
@api_view(['GET', 'POST'])
def eventlog_list(request):
    if request.method == 'GET':
        eventlogs = User.objects.all()
        page_list=MyPageNumberPagination()
        pg=page_list.paginate_queryset(queryset=eventlogs,request=request)
        # serializer = UserSerializer1(eventlogs, context={'request': request}, many=True)
        serializer = UserSerializer1(instance=pg, many=True, context={'request': request})
        return Response(serializer.data)
        # return Response(serializer.data)
    elif request.method == 'POST':
        print("request",request.data)
        serializer = UserSerializer1(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'DELETE'])
# @permission_required('OpsManage.change_user', raise_exception=True)
def user_detail(request, id, format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer1(snippet,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer1(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.delete_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)