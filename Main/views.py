from django.shortcuts import render,redirect,HttpResponse,reverse
from .models import Team,UserTasks
from .forms import TaskCreatationForm,TeamCreatationForm
from django.contrib.auth.models import User

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
    tasksDescription = getTaskInfo(request,assignee=request.user)
    return render(request,'Main/view_tasks.html',{"tasks":tasksDescription})

def getTaskInfo(request,assigner = None,assignee = None): #assigner is the Team object and assignee is user object
    #returns task's info(tile,desc,status,pk) related to assignee
    tasksDescription = {} #stores primary key as Key of dict,and task's title,dsc,status in form of dictionary as Value
    if assigner == None:
        tasks = UserTasks.objects.filter(task_assignee = assignee )
    elif assignee == null:
        tasks = UserTasks.objects.filter(task_assigner = assigner)
    for task in tasks:
        tempDict = {}
        title = task.task_title
        desc = task.task_description 
        status = task.task_status
        tempDict['title'] = title
        tempDict['description'] = desc
        tempDict['status'] = status
        tasksDescription[task.pk] = tempDict
    return tasksDescription

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

def teams(request,team_name):
    team_info,unfinished_tasks,form = team_home(request)
    option = request.GET.get("option")
    team_description = {}
    team_members = {}
    team_tasks = {}

    if team_name!='home':
        team = Team.objects.get(name = team_name)
        if option == "description":
            team_description = team.description
        elif option == "tasks":
            team_tasks = getTaskInfo(request,assigner=team)
        elif option == "members":
            team_members = {}
            members = team.members
            for member in members:
                team_members["username"] = member.username
    
    context = {"teams":team_info,
            "form":form,
            "unfinished_tasks":unfinished_tasks,
            "main_description":team_description,
            "team_tasks":team_tasks,
            "team_members":team_members}
    return render(request,"Main/teams.html",context)

def team_home(request):
    #returns teams and unfinished tasks
    teams = Team.objects.filter(creator = request.user)
    team_info = {} # store the team name and its description with key as team's primary key.
    unfinished_tasks = 0
    for team in teams: 
        _dict = {}
        _dict["name"] = team.name
        _dict["description"] = team.description
        team_info[team.pk] = _dict
        _task = UserTasks.objects.filter(task_assigner = team)
        for t in _task:
            if t.status!='done':
                unfinished_tasks+=1
    if request.method == "POST":
        form_obj = TeamCreatationForm(request.POST)
        if form_obj.is_valid():
            db_instance = form_obj.save(commit=False)
            db_instance.creator = request.user
            db_instance.save()
            return redirect(reverse('teams'))
    else:
        form = TeamCreatationForm()
    return team_info,unfinished_tasks,form
