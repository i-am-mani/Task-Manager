from django.shortcuts import render,redirect,HttpResponse,reverse
from .models import Team,UserTasks
from .forms import TaskCreatationForm

def home(request):
    return render(request,"Main/base.html")

def CreateTasks(request):
    if request.method =='POST':
        form = TaskCreatationForm(request.POST)
        if form.is_valid(): 
            obj = form.save(commit=False) #gets the model object, which is in memory but not saved in database yet. #https://stackoverflow.com/questions/12848605/django-modelform-what-is-savecommit-false-used-for
            obj.task_assignee = request.user #make changes to the object before saving it, in this case we are assasigning assignee field to logged in user.
            obj.save()  
            form = TaskCreatationForm()
            return redirect(reverse("view_tasks"))
    else:
        form = TaskCreatationForm()
    return render(request,"Main/create_tasks.html",{'form':form})

def ViewTasks(request):
    tasks = UserTasks.objects.filter(task_assignee = request.user )
    tasksDescription = {}
    for task in tasks:
        tempDict = {}
        title = task.task_title
        desc = task.task_description 
        status = task.task_status
        tempDict['title'] = title
        tempDict['description'] = desc
        tempDict['status'] = status
        tasksDescription[task.pk] = tempDict
        
    return render(request,'Main/view_tasks.html',{"tasks":tasksDescription})

def EditTasks(request):

    _pk = request.GET.get('pk')
    task = UserTasks.objects.get(pk= _pk)
    editTaskForm = TaskCreatationForm(instance = task)

    if( request.method == 'POST'):
        editTaskForm = TaskCreatationForm(request.POST,instance = task)
        if(editTaskForm.is_valid()):
            editTaskForm.save()
            return redirect("/ViewTasks/")

    return render(request,'Main/edit_tasks.html',{'form':editTaskForm})

def taskStatus(request):
    task_title = request.GET['task_title']
    task = UserTasks.objects.get(task_assignee=request.user,task_title=task_title)
    task.task_status = 'done'
    task.save() 
    return HttpResponse("done")
