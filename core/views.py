from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages

from user_profile.models import Profile

# Create your views here.

def home(request):

    #show home page
    return render(request, 'core/home.html', {
        'title': 'Home'
    })

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            #authenticated credentails
            auth.login(request, user)
            messages.success(request, 'Login successful.')
            return redirect ('core:home')
        else:
            #not able to authenticate
            messages.error(request, 'Invalid credentails, try again.')
            return redirect ('core:signin')
    #show signin page
    return render (request, 'core/signin.html' , {
        'title': 'Signin'
    })

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email'] 
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email already exists.")
                return redirect('core:signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, "This username already exists.")
                return redirect('core:signup')
            else:       
                #save new_user creds
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()
                #Log user in using new_user creds
                user_credentials = auth.authenticate(username=username, password=password)
                auth.login(request, user_credentials)
                #Create a profile for the user
                get_new_user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=get_new_user)
                new_profile.save()
                messages.success(request, "Your Account Is Created")
                return redirect('core:home')
        else:
            messages.error(request, "Passwords don't match")
            return redirect ('core:signup')

    # If request method is not POST, show signup page
    return render(request, 'core/signup.html', {
        'title': 'Signup'
    })

def signout(request):
    auth.logout(request)
    messages.success(request, "You have logged out. See you again soon!")
    return redirect('core:signin')