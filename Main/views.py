from django.shortcuts import render,redirect,HttpResponse,reverse
from .models import Team,UserTasks
from .forms import TaskCreatationForm,TeamCreatationForm,AddUserToTeam,TeamTaskCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
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
    elif assignee == None:
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
    option = request.GET.get("option","")
    team_description = {}
    team_members = {}
    team_tasks = {}
    add_member_form = {}
    add_task_form = {}

    if team_name!='home':
        team = Team.objects.get(name = team_name)
        if option == "description":
            team_description = team.description
        elif option == "tasks":
            team_tasks = getTaskInfo(request,assigner=team)
            add_task_form = add_task_from_team(request,team)
        elif option == "members":
            team_members = {}
            members = team.members.all()
            for member in members:
                team_members[member.pk] = member.username
            add_member_form = add_member_to_team(request,team)
    context = {"teams":team_info,
            "form":form,
            "title":option.capitalize(),
            "unfinished_tasks":unfinished_tasks,
            "main_description":team_description,
            "team_tasks":team_tasks,
            "team_members":team_members,
            "add_member_form":add_member_form,
            "selected_team":team_name,
            "add_task_form":add_task_form}
    return render(request,"Main/team_content.html",context)

def team_home(request):
    #returns teams and unfinished tasks
    teams = Team.objects.filter(creator = request.user)
    team_info = {} # store the team name and its description with key as team's primary key.
    for team in teams: 
        unfinished_tasks = 0
        _dict = {}
        _dict["name"] = team.name
        _dict["description"] = team.description
        _task = UserTasks.objects.filter(task_assigner = team)
        for t in _task:
            if t.task_status!='done':
                unfinished_tasks+=1
        _dict["unfinished_tasks"]=unfinished_tasks
        team_info[team.pk] = _dict
    if request.method == "POST":
        form = TeamCreatationForm(request.POST,prefix="teamCreationForm")
        if form.is_valid():
            db_instance = form_obj.save(commit=False)
            db_instance.creator = request.user
            db_instance.save()
            messages.success(request,"Team has been successfully created")
    else:        
        form = TeamCreatationForm(prefix="teamCreationForm")
    return team_info,unfinished_tasks,form

def add_member_to_team(request,team):

    if(request.method =='POST'):
        form = AddUserToTeam(request.POST,prefix="addUserToTeam")
        if(form.is_valid()):
            un=form.cleaned_data['member_username']
            if(User.objects.filter(username=un).exists()):
                team.members.add(User.objects.get(username=un))
            else:
                messages.error(request,"Failed to add member : Please check the Username and try again")

    else:
        form = AddUserToTeam(prefix = "addUserToTeam")
    return form

def add_task_from_team(request,team):
    if(request.method == 'POST'):
        form = TeamTaskCreationForm(request.POST,prefix = "addTaskFromTeam")
        if(form.is_valid()):
            assignee = form.cleaned_data['assignee']
            obj = form.save(commit=False)
            obj.task_assigner = team
            
            user_db = User.objects.filter(username=assignee)
            if(user_db.exists):
                obj.task_assignee = user_db[0]
                obj.save()
            else:
                messages.error(request,"The Assignee Usename is incorrect!")
    else:
        form = TeamTaskCreationForm(prefix="addTaskFromTeam")
    return form


            
