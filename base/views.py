from django.shortcuts import render
from .models import User
from django.contrib.auth.hashers import make_password

# Create your views here.

def home(request):
    queryset = User.objects.all()
    return render(request,'index.html',context={'users':queryset})

def register(request):
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