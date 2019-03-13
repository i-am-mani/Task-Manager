from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Team(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='creator')
    name = models.CharField(max_length=200,unique=True)
    description = models.CharField(max_length=3000,null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    date_of_creation = models.DateField(auto_now=True)


class UserTasks(models.Model):
    PLANNED='planned'
    INPROGRESS = 'inprogress'
    DONE = 'done'
    _choices = [(PLANNED,'planned'),(INPROGRESS,'inprogress'),(DONE,'done')]

    #fields
    task_assignee =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)  #https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
    task_assigner =  models.ForeignKey(Team,on_delete=models.CASCADE,null=True)
    task_title = models.CharField(max_length=255,unique=True) 
    task_description = models.CharField(max_length=4000)
    task_status = models.CharField(choices = _choices,default=PLANNED,max_length=255)
    date_of_creation = models.DateField(auto_now=True)
    task_comments = models.CharField(max_length=3000,null=True)












#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/