from django.shortcuts import render,redirect,HttpResponse,reverse
from .models import Team,UserTasks
from .forms import TaskCreatationForm,TeamCreatationForm,AddUserToTeam,TeamTaskCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
def home(request):
    return render(request,"Main/home.html")
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

def getTaskInfo(request,assigner = None,assignee = None):
    #assigner is the Team object and assignee is user object
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
    task_pk = request.GET.get('pk')
    task = UserTasks.objects.get(pk=task_pk)
    task.task_status = 'done'
    task.save() 
    messages.success(request,"The Task has been marked as complete!")
    return ViewTasks(request)

def teams(request,team_name):
    team_info,form = team_home(request)
    option = request.GET.get("option","")
    team_description = {}
    team_members = {}
    team_tasks = {}
    add_member_form = {}
    add_task_form = {}
    team_desc = {}

    if team_name!='home':
        team = Team.objects.get(name = team_name)
        if option == "description":
            team_description = team.description
            mem_count = team.members.all().count()
            ts_count = UserTasks.objects.filter(task_assigner = team).count()
            team_desc = {"team_description":team_description,"mem_count":mem_count,"ts_count":ts_count}
            
        elif option == "tasks":
            team_tasks = getTaskInfo(request,assigner=team)
            add_task_form = add_task_from_team(request,team)
        elif option == "members":
            team_members = {}
            members = team.members.all()
            for member in members:
                team_members[member.pk] = member.username
            add_member_form = add_member_to_team(request,team)
        


    context = {
            "teams":team_info, #consist of all team's name,desc,unfinished tasks
            "form":form, #Form for creating new Team 
            "title":option.capitalize(), #Selected option for a specific team
            "team_tasks":team_tasks, #dictionary of all tasks belonging to a team
            "team_members":team_members, #member list of the team
            "add_member_form":add_member_form, # For for adding new member to team
            "selected_team":team_name, #Selected team's name
            "add_task_form":add_task_form, # Form for creating new Task
            "team_desc":team_desc  #Consists of Teams description,consits of selected team's description,member and task count 
            }
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
    return team_info,form

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


def profile(request):
    user_profile = {}
    user = request.user

    user_profile["Username"] = request.user.username
    user_profile["First Name"] = request.user.first_name
    user_profile["Last Name"] = request.user.last_name
    user_profile["Email"] = request.user.email

    team_db = request.user.team_set.all()
    team_db_creator = request.user.creator.all()
    user_teams = {}
    for team in team_db:
        user_teams[team.name] = "member"
    for team in team_db_creator:
        user_teams[team.name] = "creator"
    print(user_teams)
    return render(request,"Main/profile.html",{"user_profile":user_profile,"user_teams":user_teams})
