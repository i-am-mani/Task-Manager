
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    first_name = forms.CharField(label='First name', max_length=30)
    last_name = forms.CharField(label='Last name', max_length=40)
    email = forms.EmailField()

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['username'].widget.attrs.update({"class":"form-control","placeholder":"Enter Username"})
        self.fields['first_name'].widget.attrs.update({"class":"form-control","placeholder":"Enter First Name"})
        self.fields['last_name'].widget.attrs.update({"class":"form-control","placeholder":"Enter Last Name"})
        self.fields['email'].widget.attrs.update({"class":"form-control","placeholder":"Enter e-mail"})
        self.fields['password1'].widget.attrs.update({"class":"form-control","placeholder":"Enter Password"})
        self.fields['password2'].widget.attrs.update({"class":"form-control","placeholder":"Re-Enter Password"})
        
    class Meta:
        model = User 
        fields = ['username','first_name','last_name','email','password1','password2']