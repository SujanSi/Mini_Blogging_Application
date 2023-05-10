from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group



# Create your views here.


def index(request):
    post=Post.objects.all()
    return render(request,'index.html',{'post':post})

def nav(request):
    return render(request,'nav.html')

def about(request):
    return render(request,'aboutus.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email=form.cleaned_data['email']
            address=form.cleaned_data['address']
            message=form.cleaned_data['message']
            contact = Contact(name = name,email=email,address=address,message=message)
            contact.save()
            form = ContactForm()
            return redirect('/contact/')
        else:
            form = ContactForm()

        return render(request,'contactus.html',{'form':form})
    else:
        form = ContactForm()
        return render(request,'contactus.html',{'form':form})

def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: # check if the user is an admin
            post = Post.objects.all() # fetch all posts
        else:
            post = Post.objects.filter(author=request.user)
        return render(request,'dashboard.html',{'post':post})
    else:
        return redirect('/login/')
    


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/dashboard/')
                else:
                    messages.error(request, "Invalid username or password.")
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('/dashboard/')

def user_logout(request):
    logout(request)
    return redirect('/login/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email= form.cleaned_data['email']
            password=form.cleaned_data['password1']
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect('/login/')
    else:
        form = SignupForm()
            
    return render(request,'signup.html',{'form':form})


def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Addpost(request.POST,request.FILES)
            if form.is_valid():
                author = request.user.username
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                image = form.cleaned_data['image']
                pst = Post(author=author,title=title,content=content)
                pst.image = image # set the value of the image field
                pst.save()
                return redirect('/dashboard/')
        else:
            form = Addpost()

        return render(request,'addpost.html',{'form':form})
    else:
        return redirect('/login/')
    
def edit_view(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.get(id=id)
            form = Addpost(request.POST,request.FILES,instance=post)
            if form.is_valid():
                post.save()
                return redirect('/dashboard/')
        else:
            post = Post.objects.get(id=id)
            form=Addpost(instance=post)
        return render(request,'edit.html',{'form':form})      
    return redirect('/dashboard/')
    
def delete_view(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('/dashboard/')