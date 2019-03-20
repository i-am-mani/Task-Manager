from django.test import TestCase
from .forms import UserForm
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):

    c_data = {"first_name":"user one","last_name":"rookie",
    "username":"NewUser","password1":"Task@2019",
    "password2":"Task@2019","email":"abc@gmail.com"}

    user_model = get_user_model()

    @classmethod
    def setUpTestData(cls):
        """
            Create User with correct data
        """
        form = UserForm(UserModelTest.c_data) 
        form.save()

    def test_sign_up_cdata(self):
        """
            Using same form data
        """
        form = UserForm(UserModelTest.c_data)
        self.assertFalse(form.is_valid())
        
    def test_user_added_to_db(self):
        """
            Test if signing up with correct data, adds user to db.
        """
        number_of_users = len(UserModelTest.user_model.objects.all())
        self.assertEqual(number_of_users,1)

    def test_login(self):
        """
            Test login  with correct Data.
        """
        login_status = self.client.login(username="NewUser",password="Task@2019")
        self.assertTrue(login_status)
    
    def test_login_w_name_pass(self):
        """
            Test login with wrong name and password
        """
        login_status = self.client.login(username='WrongUser',password="wrongpassword")
        self.assertFalse(login_status)
    
    def test_login_w_name(self):
        """
            Test login with wrong username
        """
        login_status = self.client.login(username='WrongUser',password="Task@2019")
        self.assertFalse(login_status)

    def test_login_w_pass(self):
        """
            Test Login with wrong password
        """
        login_status = self.client.login(username='NewUser',password="wrongpassword")
        self.assertFalse(login_status)
    
        