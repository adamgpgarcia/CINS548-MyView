from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from view.forms import JoinForm, LoginForm
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def view(request):
    return render(request, 'view/view.html')
def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = { "join_form": join_form }
            return render(request, 'view/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'view/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                logger.warning("Someone tried to login and failed.")
                logger.warning("They used username: {} and password: {}".format(username,password))
                return render(request, 'view/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.

        return render(request, 'view/login.html', {"login_form": LoginForm})
@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")
