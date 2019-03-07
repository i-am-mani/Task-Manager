from django.shortcuts import render,redirect
from .forms import UserForm


def registerNewUser(request):
        # if this is a POST request we need to process the form data 
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = UserForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                form.save()

                # username = form.cleaned_data.get('username')

                # messages.success(request, f'Account created for {username}!')

                return redirect('login')

        # if a GET we'll create a blank form
        else:
            form = UserForm()

        return render(request, 'Users/register.html', {'form': form})
    else:
        return redirect("home")
    return render(request,"Users/register.html",{"form":form})
