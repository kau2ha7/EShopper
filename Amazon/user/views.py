from django.shortcuts import render,redirect
from .forms import MyLoginForm,MyUserRegistrationForm
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
from .models import Profile



# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = MyLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username = data['username'],password = data['password'])
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return redirect('/login')   
    else:
        form = MyLoginForm()        
    return render(request,'user/login.html',{'form':form})    
    
def user_register(request):
    if request.method == 'POST':
        print(request.POST)
        form = MyUserRegistrationForm(request.POST)  
        print('form: ', form)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password2'])
            new_user.save()
            Profile.objects.create(user = new_user)
            return render(request,'user/login.html')
    else:
        form = MyUserRegistrationForm()         
    return render(request,'user/register.html',{'form':form})
