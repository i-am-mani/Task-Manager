from django.db import models
from django import forms
from .models import Team,UserTasks,TaskComment
from django.contrib.auth.models import User


class TaskCreationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(TaskCreationForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['task_title'].widget.attrs.update({"class":"form-control","placeholder":"Enter Title for task"})
        self.fields['task_description'].widget = forms.Textarea(attrs={"class":"form-control ","placeholder":"Enter Description for the task"})
    class Meta:
        model = UserTasks
        fields =['task_title','task_description']

class TeamCreationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(TeamCreationForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs.update({"class":"form-control","placeholder":"Enter Name for Team"})
        self.fields['description'].widget.attrs.update({"placeholder":"Enter A Short Description About Your Team"})
    class Meta:
        model = Team
        fields = ['name','description']

class AddUserToTeam(forms.Form):
    member_username = forms.CharField(label="Member Username",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username of the member you wish to add'}))

class TeamTaskCreationForm(TaskCreationForm):
    assignee = forms.CharField(label="Assignee",widget=forms.TextInput(attrs={"class":'form-control','placeholder':'Assign the task to ?'}))

class TaskCommentForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        a = {
        'class':'form-control text-muted',
        'placeholder':'Enter Your Comment',
        'style':'font-size:15px' }
        super(TaskCommentForm,self).__init__(*args,**kwargs)
        self.fields['comment_content'].widget.attrs.update(a)
        self.fields['comment_content'].label = ""
    class Meta:
        model = TaskComment
        fields = ['comment_content']