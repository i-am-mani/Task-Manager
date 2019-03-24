from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from .forms import *
from .models import UserTasks,Team


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        details = {
            "username": "testUser1",
            "first_name": "test",
            "last_name": "user",
            "password": "StrongPassword@123",
            "email": "testUser@nomail.com"
            }
        cls.user_model = get_user_model()
        cls.test_user = cls.user_model.objects.create_user(**details)
        
 
    def test_task_without_login(self):
        # attempting to view tasks before log-in should redirect to login page
        response_view_tasks = self.client.get(reverse("view_tasks"))
        response_create_tasks = self.client.get(reverse("create_tasks"))

        self.assertEquals(response_view_tasks.status_code, 302)
        self.assertEquals(response_create_tasks.status_code, 302)

class TestForms(TestCase):

    @classmethod
    def setUpTestData(cls):
        details = {
            "username": "testUser1",
            "first_name": "test",
            "last_name": "user",
            "password": "StrongPassword@123",
            "email": "testUser@nomail.com"
            }
        cls.user_model = get_user_model()
        cls.test_user = cls.user_model.objects.create_user(**details)

    def test_create_user_tasks(self):
        form_data = {
            "task_title":"Test",
            "task_description":"Test Description",
            "task_comments":"Test comment"
        }
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        obj = form.save(commit = False)
        obj.task_assignee = TestForms.user_model.objects.get(username="testUser1")
        obj.save()

        task_count = UserTasks.objects.all().count()
        self.assertEqual(task_count,1)
        
        # Use same data - invalid 
        form2 = TaskCreationForm(data=form_data) 
        self.assertFalse(form2.is_valid())

        # Not Providing description - invalid 
        form3_data = {
            "task_title":"Test 3",
            "task_description":"",
            "task_comments":"Test comment"
        }
        form3 = TaskCreationForm(data=form3_data)
        self.assertFalse(form3.is_valid())

    def test_team_creation(self):
        form_data = {
            "name":"Team-1",
            "description":"Here is the description"}
        form1 = TeamCreationForm(data=form_data)
        self.assertTrue(form1.is_valid())
        obj = form1.save(commit=False)
        obj.creator = TestForms.user_model.objects.get(username = "testUser1")
        obj.save()

        team_count = Team.objects.all().count()
        self.assertEqual(team_count,1)

        # Use Same Data -invalid
        form2 = TeamCreationForm(data=form_data)
        self.assertFalse(form2.is_valid())


        # Adding members
        self.createUsers()
        team_member_count = Team.objects.get(name="Team-1").members.all().count()
        self.assertEqual(team_member_count,8)
    
    def createUsers(self):
        for i in range(2,10):
            details = {
                "username": "testUser"+str(i),
                "first_name": "test",
                "last_name": "user",
                "password": "StrongPassword@123",
                "email": "testUser"+str(i)+"@nomail.com"
                }
            u = TestForms.user_model.objects.create_user(**details)
            team = Team.objects.get(name="Team-1")
            team.members.add(u)
            
        
        
