from django.shortcuts import render,redirect
from .models import Team,UserTasks
from .forms import TaskCreatationForm
def home(request):
    return render(request,"Main/base.html")

def UserTasks(request):
    if request.method =='POST':
        form = TaskCreatationForm(request.POST)

        if form.is_valid(): 
            obj = form.save(commit=False) #gets the model object, which is in memory but not saved in database yet. #https://stackoverflow.com/questions/12848605/django-modelform-what-is-savecommit-false-used-for
            obj.task_assignee = request.user #make changes to the object before saving it, in this case we are assasigning assignee field to logged in user.
            obj.save()  
            
            redirect('home')
    else:
        form = TaskCreatationForm()
    return render(request,"Main/tasks.html",{'form':form})