from django import forms
from work.models import User,Taskmodel

class Register(forms.ModelForm):

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your name'}),
            'first_name':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your last name'}),
            'email':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter password'})
        }

class Taskform(forms.ModelForm):
    
    class Meta:
        model=Taskmodel
        fields=['task_name','task_description']
        widgets={
            'task_name':forms.TextInput(attrs={'class':'form-control',
                                               'placeholder': 'Enter the task'}),
            'task_description':forms.Textarea(attrs={'class':'form-control','column':10,'row':5,
                                                     'placeholder': 'Enter the task'}),
        }

class Loginform(forms.Form):

    user_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                            'placeholder':'Username'}))
    password=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                           'placeholder':'password'}))