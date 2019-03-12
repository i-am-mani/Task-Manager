from django.db import models
from django import forms
from .models import Team,UserTasks


class TaskCreatationForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(TaskCreatationForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['task_title'].widget.attrs.update({"class":"form-control","placeholder":"Enter Title for task"})
        self.fields['task_description'].widget = forms.Textarea(attrs={"class":"form-control ","placeholder":"Enter Description for the task"})
        self.fields['task_comments'].widget = forms.Textarea(attrs={"class":"form-control ","placeholder":"Comments for task","rows":"5"})
        self.fields['task_comments'].required = False
        
    class Meta:

        model = UserTasks
        fields =['task_title','task_description','task_comments']

class EditTasksForm(forms.Form):

    def __init__(self,user,*args,**kwargs):
        self.field['task_to_edit']
    

    task_to_edit = forms.CharField(max_length=255,widget = forms.TextInput(attrs={'class':'form-control',"placeholder":"Enter New title"}))

    new_title = forms.CharField(max_length=255,widget = forms.TextInput(attrs={'class':'form-control',"placeholder":"Enter New title"}))
    new_description = forms.CharField(max_length=4000,widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Enter New Description'}))



