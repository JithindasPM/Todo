from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import Register,Loginform,Taskform
from work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.

def Login_required(fn):
    def wrapper(request,**kwargs):
        if not request.user.is_authenticated:
            return redirect('log')
        else:
            return fn(request,**kwargs)
    return wrapper

def Mylog(fn):
    def wrapper(request,**kwargs):
        id=kwargs.get('pk')
        data=Taskmodel.objects.get(id=id)
        if data.user!=request.user:
            return redirect('log')
        else:
            return fn(request,**kwargs)
    return wrapper

class Registration(View):

    def get(self,request,**kwargs):
        form=Register()
        return render(request,"index.html",{"form":form})
    
    def post(self,request,**kwargs):
        form=Register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
        return redirect('log')
    
class Signin(View):

    def get(self,request,**kwargs):
        form=Loginform()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            user=form.cleaned_data.get("user_name")
            psw=form.cleaned_data.get("password")

            user_obj=authenticate(username=user,password=psw)
            if user_obj:
                login(request,user_obj)
                return redirect('todo')
            else:
                form=Loginform()
                return render(request,"login.html",{"form":form})
            
@method_decorator(Login_required,name='dispatch')
class Add_task(View):
    def get(self,request,**kwargs):

        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        form=Taskform()
        return render(request,"todo.html",{'form':form,"data":data})
    
    def post(self,request,**kwargs):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"Task Added Successfully")
        form=Taskform()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,'todo.html',{'form':form,'data':data})

@method_decorator(Login_required,name='dispatch')
@method_decorator(Mylog,name='dispatch')
class Delete_task(View):
    def get(self,request,**kwargs):
        id=kwargs.get('pk')
        Taskmodel.objects.get(id=id).delete()
        return redirect('todo')
    
@method_decorator(Login_required,name='dispatch')
@method_decorator(Mylog,name='dispatch')
class Update(View):
    def get(self,request,**kwargs):
        id=kwargs.get('pk')
        obj=Taskmodel.objects.get(id=id)
        if obj.completed==False:
            obj.completed=True
            obj.save()
            return redirect('todo')
        else :
            obj.completed=False
            obj.save()
            return redirect('todo')

@method_decorator(Login_required,name='dispatch')
class Logout_view(View):
    def get(self,request,**kwargs):
        logout(request)
        return redirect('log')
    
class Del_User_View(View):
    def get(self,request,**kwargs):
        id=kwargs.get('pk')
        User.objects.get(id=id).delete()
        return redirect('log')
    
class Update_User_View(View):
    def get(self,request,**kwargs):
        id=kwargs.get('pk')
        data=User.objects.get(id=id)
        form=Register(instance=data)
        return
        
