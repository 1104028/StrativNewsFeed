from django.shortcuts import render, redirect
import requests
from .forms import NewUserForm, LoginForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.
from django.http import HttpResponse

def getapinews(request):
    option = request.GET['option']
    if option == 'country':
        r = requests.get(
            'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=870fc67670de409b8243be8052873a8e',
            params=request.GET)
    elif option == 'source':
        r = requests.get(
            'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=870fc67670de409b8243be8052873a8e',
            params=request.GET)
    if r.status_code == 200:
        result = r.json()
        titles = []
        for news_item in result['articles']:
            titles.append(news_item['title'])

        return render(request,
                      'NewsFeed/news.html', {'titles': titles})

    return HttpResponse('Could not find data')


def registration(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            response = redirect("allnews")
            response['Location'] += '?option=country'
            return response
        else:
            messages.error(request,"Invalid password, please provide at least 8 character password")
    else:
        form = NewUserForm()
        return render(request, "NewsFeed/auth/register.html", {"register_form": form})


def userlogin(request):
    if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        response = redirect("allnews")
                        response['Location'] += '?option=country'
                        return response
                else:
                    messages.error(request,"Incorrect User name or Password")
                # return redirect("login")
    return render(request, "NewsFeed/auth/login.html")


def userlogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

def forgotpassword(request):
    pass