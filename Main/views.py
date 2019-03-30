from django.shortcuts import render, redirect, HttpResponse, reverse, get_object_or_404
from .models import Team, UserTasks, TaskComment
from .forms import (TeamCreationForm, TeamTaskCreationForm,
                    TaskCreationForm, AddUserToTeam, TaskCommentForm)
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "Main/home.html")


def CreateUserTasks(request):
    """
        Return Task creation form
    """
    if request.method == 'POST':
        form = TaskCreationForm(request.POST, prefix="createUserTask")
        if form.is_valid():
            # gets the model object, which is in memory but not saved in database yet.
            # #https://stackoverflow.com/questions/12848605/django-modelform-what-is-savecommit-false-used-for
            obj = form.save(commit=False)
            obj.task_assignee = request.user
            obj.task_assigner = request.user
            obj.save()
            messages.success(request, "New task has been added")
            return TaskCreationForm(prefix="createUserTask")
    else:
        form = TaskCreationForm(prefix="createUserTask")
    return form


def CreateCommentOnTask(request):
    """
        return Comment form.
    """
    if request.method == 'POST':
        task_id = request.POST.get('task_id', '')
        form = TaskCommentForm(request.POST, prefix="taskCommentForm")
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.save()
            # task_comment = TaskComment.objects.filter(task_id = task_id)
            task = UserTasks.objects.get(pk=task_id)
            task.task_comments.add(form_obj)
            task.save()
            messages.success(request, "Comment Added!")
            return TaskCommentForm(prefix="taskCommentForm")
    else:
        form = TaskCommentForm(prefix="taskCommentForm")
    return form


@login_required()
def ViewUserTasks(request):
    """
        View finished/unfinished tasks with their dscription and status.
    """
    form_user_task = CreateUserTasks(request)
    form_task_comment = CreateCommentOnTask(request)

    tasksDescription = getTaskInfo(request, assignee=request.user)

    context = {
        "tasks": tasksDescription,
        "form_task": form_user_task,
        "form_comment": form_task_comment}
    return render(request, 'Main/view_tasks.html', context)


def getTaskInfo(request, team=None, assignee=None):
    """
        Return all the tasks of the assignee's or teams's,
        data as dictionary, each task is stored with key 
        as it primary key value as a dictionary with keys as title,
        description,status.

        Arguments:
            team(Team):Team object of the Assigner
            assignee(User):The User to which the Task is to be Assigned
        Return:
            task_description(Dictionary):{pk:{title:"__",dsc:"__",status:"__"}}

    """
    tasksDescription = {}  # stores primary key as Key of Task,and task's title,dsc,status in form of dictionary as Value
    if team == None:

        tasks = UserTasks.objects.filter(task_assignee=assignee)
    elif assignee == None:
        tasks = UserTasks.objects.filter(task_team=team)

    for task in tasks:
        tempDict = {}
        title = task.task_title
        desc = task.task_description
        status = task.task_status
        assigner = task.task_assigner
        assignee = task.task_assignee
        tempDict['title'] = title
        tempDict['description'] = desc
        tempDict['status'] = status
        tempDict['assigner'] = assigner
        tempDict['assignee'] = assignee

        commentDict = {}  # Stored in form date:comment
        comments = task.task_comments.all()
        if comments:
            for c in comments:
                comment_date = c.date_of_creation
                comment_content = c.comment_content
                if(comment_date in commentDict):
                    commentDict[comment_date].append(comment_content)
                else:
                    commentDict[comment_date] = [comment_content]

        tempDict['comments'] = commentDict

        tasksDescription[task.pk] = tempDict

    return tasksDescription


def EditTasks(request):
    """
        View for Editing Tasks, It uses the primary key of the task to be edited
        and returns a editTaskForm, which is filled with current values of the task.
        If the Post data is valid then the task is modified to new values in db and 
        redirects user to View Task page

        Return:
            render(): rendering edit_tasks.html and editTaskForm as the context.
    """
    _pk = request.GET.get('pk')
    task = UserTasks.objects.get(pk=_pk)
    editTaskForm = TaskCreationForm(instance=task, prefix="editTaskForm")

    if(request.method == 'POST'):
        editTaskForm = TaskCreationForm(
            request.POST, instance=task, prefix="editTaskForm")
        if(editTaskForm.is_valid()):
            editTaskForm.save()
            messages.success("Task Has been edited Successfuly")
            return redirect("/ViewTasks/")

    return render(request, "Main/edit_tasks.html", {"form": editTaskForm})


def task_mark_status_complete(request):
    """
        Mark the Task's status as 'done', Task is identified by primary key 
        passed as GET parameter.
    """

    task_pk = request.GET.get('pk')
    task = UserTasks.objects.get(pk=task_pk)
    task.task_status = 'done'
    task.save()
    messages.success(request, "The Task has been marked as complete!")
    return ViewUserTasks(request)


@login_required()
def teams(request, team_name):
    """
        Render the Team page.
    """
    team_info, form = team_home(request)
    option = request.GET.get("option", "")
    team_description = {}
    team_members = {}
    team_tasks = {}
    add_member_form = {}
    add_task_form = {}
    team_desc = {}
    form_comment = {}
    position = "member"

    if team_name != 'home':
        team = Team.objects.get(name=team_name)
        position = "creator" if team.creator == request.user else "member"
        if option == "description":
            team_description = team.description
            mem_count = team.members.all().count()
            ts_count = UserTasks.objects.filter(task_team=team).count()
            team_desc = {"team_description": team_description,
                         "mem_count": mem_count, "ts_count": ts_count}

        elif option == "tasks":
            team_tasks = getTaskInfo(request, team=team)
            add_task_form = add_task_from_team(request, team)
            form_comment = CreateCommentOnTask(request)

        elif option == "members":
            team_members = {}
            members = team.members.all()
            for member in members:
                team_members[member.pk] = member.username
            add_member_form = add_member_to_team(request, team)

    context = {
        "teams": team_info,  # consist of all team's name,desc,unfinished tasks
        "form": form,   # Form for creating new Team
        "title": option.capitalize(),  # Selected option for a specific team
        "team_tasks": team_tasks,  # dictionary of all tasks belonging to a team
        "team_members": team_members,  # member list of the team
        "add_member_form": add_member_form,  # For for adding new member to team
        "selected_team": team_name,  # Selected team's name
        "add_task_form": add_task_form,  # Form for creating new Task
        # Consists of Teams description,consits of selected team's description,member and task count
        "team_desc": team_desc,
        "form_comment": form_comment,  # Form for Commenting on task
        "position": position
    }
    return render(request, "Main/team_content.html", context)


def team_home(request):
    """
        return teams and unfinished tasks count. 
    """
    teams = Team.objects.filter(members__in=[request.user])
    # store the team name and its description with key as team's primary key.
    team_info = {}
    for team in teams:
        unfinished_tasks = 0
        _dict = {}
        _dict["name"] = team.name
        _dict["description"] = team.description
        _task = UserTasks.objects.filter(task_team=team)
        for t in _task:
            if t.task_status != 'done':
                unfinished_tasks += 1
        _dict["unfinished_tasks"] = unfinished_tasks
        team_info[team.pk] = _dict
    if request.method == "POST":
        form = TeamCreationForm(request.POST, prefix="teamCreationForm")
        if form.is_valid():
            db_instance = form.save(commit=False)
            db_instance.creator = request.user
            db_instance.save()
            db_instance.members.add(request.user)
            messages.success(request, "Team has been successfully created")
    else:
        form = TeamCreationForm(prefix="teamCreationForm")
    return team_info, form


def add_member_to_team(request, team):
    """
        Add User with valid Username as member of the team. 

        Arguments:
            team(str): Team's name to which member is to be added
        Return:
            Form(AddUserToTeam): Return AddUserToTeam form 
    """
    if(request.method == 'POST'):
        form = AddUserToTeam(request.POST, prefix="addUserToTeam")
        if(form.is_valid()):
            un = form.cleaned_data['member_username']
            if(User.objects.filter(username=un).exists()):
                team.members.add(User.objects.get(username=un))
            else:
                messages.error(
                    request, "Failed to add member : Please check the Username and try again")

    else:
        form = AddUserToTeam(prefix="addUserToTeam")
    return form


def add_task_from_team(request, team):
    """
        Handle Task creation from Team. Uses TeamTaskCreationForm, 
        Create and assign the task to valid user.

        Arguments:
            team(Team): The Assigner of the task.
        Return:
            form(TeamTaskCreationForm)

    """
    if(request.method == 'POST'):
        # Prefix is used to avoid POST data collision of different forms, since
        # single request is used to process many Forms.
        form = TeamTaskCreationForm(request.POST, prefix="addTaskFromTeam")
        print(request.POST)
        if(form.is_valid()):
            assignee = form.cleaned_data['assignee']
            # Get the Database object without commiting
            print(form.cleaned_data['task_description'])
            obj = form.save(commit=False)
            obj.task_assigner = request.user
            obj.task_team = team
            # Check Whether the UserName of Assignee exists in the db
            user_db = User.objects.filter(username=assignee)
            if(user_db.count() == 1):
                user = user_db[0]
                if(team in Team.objects.filter(members__in=[user])):
                    obj.task_assignee = user
                    obj.save()
                else:
                    messages.error(
                        request, "The User doesn't belong to this team")
            else:
                messages.error(request, "The Assignee Usename is incorrect!")
    else:
        form = TeamTaskCreationForm(prefix="addTaskFromTeam")
    return form


@login_required()
def profile(request, user_name):
    """
        Render Profile Page.
    """
    user_profile = {}
    user = get_object_or_404(User, username=user_name)

    if user:
        user_profile["Username"] = user.username
        user_profile["First Name"] = user.first_name
        user_profile["Last Name"] = user.last_name
        user_profile["Email"] = user.email

        team_db = request.user.team_set.all()  # All the team in which user is member
        # All the team in which user is creator
        team_db_creator = request.user.creator.all()
        user_teams = {}
        for team in team_db:
            user_teams[team.name] = "member"
        for team in team_db_creator:
            user_teams[team.name] = "creator"
        return render(request, "Main/profile.html", {"user_profile": user_profile, "user_teams": user_teams})
    return user
