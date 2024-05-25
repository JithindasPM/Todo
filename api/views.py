from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from api.serializers import *
# from rest_framework.authtoken.models import Token

# Create your views here.

class User_Register_Apiview(APIView):
    def post(self,request,*args,**kwargs):
        serializer=User_Registration_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
class Todo_Viewset(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def list(self,request,*args,**kwargs):
        qs=Taskmodel.objects.all()
        serializer=Todo_Serializer(qs,many=True)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        serializer=Todo_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
            return Response({'message':'deleted successfully'})
        else:
            return Response({'message':'no todo item'})
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            serializer=Todo_Serializer(qs)
            return Response(serializer.data)
        else:
            return Response({'message':'no todo item'})
        
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            serializer=Todo_Serializer(data=request.data,instance=qs)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message':'no todo item'})
        
    # def list(self,request,*args,**kwargs):
    #     qs=Token.objects.all()
    #     serializer=Token_Serializer(qs,many=True)
    #     return Response(serializer.data)


class Todomodel_Viewset(ModelViewSet):
    queryset=Taskmodel.objects.all()
    serializer_class=Todo_Serializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    