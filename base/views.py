from django.shortcuts import render, redirect
from .models import User,FriendRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home_view(request):
    queryset = User.objects.all()
    return render(request,'index.html',context={'users':queryset})

@login_required(login_url='login')
def friend_request_send_view(request):
    user = request.user # URL/VIEW requesting user (authenticated/authorized user)
    friend_request_queryset = FriendRequest.objects.filter(requested_by_user=user).values_list('request_user') # Filtering all friend request data where requested by user is url request user , converting onto list where the values are only request_user(request sent user)

    user_queryset = User.objects.all().exclude(id__in=friend_request_queryset).exclude(id=request.user.id) # Excluding users from all user data where id of user is in list of request sent user, also excluding url request user
    return render(request,'friendRequestSend.html',context={'users':user_queryset})

def register_view(request):
    if request.method == 'POST':
        error_message =  ''
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        hash_password = make_password(password)

        # Validations
        if username == '':
            error_message += 'Username is required!'
        
        if email == '':
            error_message += 'Email is required!'
        
        if password == '':
            error_message += 'Password is required!'


        try:
            user_queryset = User.objects.get(username=username)
        except:
            user_queryset = None

        if user_queryset != None:
            error_message += 'Username already exists!'
        

        if '@' in email:
            split_email = email.split('@')
            if '.com' not in split_email[1]:
                error_message += 'Email not valid!'
        else:
            error_message += 'Email not valid!'

        if error_message == '':
            User.objects.create(username=username,email=email,password=hash_password)
        return render(request,'register.html',context={'error':error_message} if error_message != '' else {'success':'Registered successfully!'})
    return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        error_message = ''
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validations
        if username == '':
            error_message += 'Username is required!'
        if password == '':
            error_message += 'Password is required!'

        user = authenticate(username=username,password=password)

        if user == None:
            error_message += 'Invalid credentials!'

        if error_message == '':
            login(request,user)
            return redirect('home')
        
        return render(request,'login.html',context={'error':error_message})

    return render(request,'login.html')