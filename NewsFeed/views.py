from django.shortcuts import render, redirect
import requests
from .forms import NewUserForm, LoginForm, KeywordForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Countries, Sources, Keywords, Mapper
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from Newsapi.models import NewsItem
from rest_framework.authtoken.models import Token


# showing all news based on user seetings
def getapinews(request):
    if request.user.is_authenticated:
        userallcountries = Mapper.objects.filter(user=request.user, itemName="Country").values_list('selecteddata',
                                                                                                    flat=True)
        userallsources = Mapper.objects.filter(user=request.user, itemName="Source").values_list('selecteddata',
                                                                                                 flat=True)
        userallkeyword = Keywords.objects.filter(user=request.user).values_list('keyword', flat=True)
        newsfinallist = []  # contails filtered news
        keywordfound = []  # contails mathched keywords
        send_email = False  # check keyword is found or not
        allnews = NewsItem.objects.all()

        # generate list based on user country settings
        if allnews.count() > 0:
            for news in allnews:
                if news.country in userallcountries:
                    if news.source in userallsources:
                        newsfinallist.append(news)
                        break

        # generate list based on matched keywords for user
        for keyword in userallkeyword:
            for news in newsfinallist:
                if keyword in news.title:
                    keywordfound.append(keyword)
                    send_email = True
                    break

        # send email to user if keywords found on the news title
        if send_email:
            subject = 'News Found at NewsFeed '
            message = f'Hi {request.user}, We found some news which matching with your keyword, {keywordfound}'
            email_from = settings.EMAIL_HOST_USER
            userinfo = User.objects.get(pk=request.user.id)
            recipient_list = [userinfo.email]

            send_mail(subject, message, email_from, recipient_list)

            # paginate front end news list
        paginator = Paginator(newsfinallist, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,
                      'NewsFeed/news.html', {'page_obj': page_obj})
    return redirect('login')


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
            messages.error(request, "Invalid password, please provide at least 8 character password")
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
                login(request, user)
                response = redirect("allnews")
                response['Location'] += '?option=country'
                return response
            else:
                messages.error(request, "Incorrect User name or Password")
            # return redirect("login")
    return render(request, "NewsFeed/auth/login.html")


def userlogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


def forgotpassword(request):
    pass


def usercountry(request):
    userallcountries = Mapper.objects.filter(user=request.user, itemName="Country").values_list('selecteddata',
                                                                                                flat=True)
    if request.method == "POST":
        selectedcountries = request.POST.getlist('selectedcountries')
        insertedlist = []
        for item in selectedcountries:
            if item not in userallcountries:
                insertedlist.append(
                    Mapper.objects.create(itemName='Country', selecteddata=item,
                                          user=User.objects.get(pk=request.user.id)))
        try:
            Mapper.objects.bulk_create(insertedlist, batch_size=None, ignore_conflicts=False)
        except:
            pass
        response = redirect("allnews")
        response['Location'] += '?option=country'
        return response

    all_countries = Countries.objects.all()
    return render(request, "NewsFeed/countrysettings.html",
                  {'allcountries': all_countries, 'userallcountries': userallcountries})


def usersource(request):
    userallsources = Mapper.objects.filter(user=request.user, itemName="Source").values_list('selecteddata', flat=True)
    if request.method == "POST":
        selectedsources = request.POST.getlist('selectedsources')
        insertedlist = []
        for item in selectedsources:
            if item not in userallsources:
                insertedlist.append(
                    Mapper.objects.create(itemName='Source', selecteddata=item,
                                          user=User.objects.get(pk=request.user.id)))
        try:
            Mapper.objects.bulk_create(insertedlist, batch_size=None, ignore_conflicts=False)
        except:
            pass
        response = redirect("allnews")
        response['Location'] += '?option=country'
        return response

    all_sources = Sources.objects.all()
    return render(request, "NewsFeed/sourcesettings.html",
                  {'allsources': all_sources, 'userallsources': userallsources})


def addkeywords(request):
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            add_keyword = Keywords.objects.create(
                user=User.objects.get(pk=request.user.id),
                keyword=form.cleaned_data["keywordname"]
            )
            add_keyword.save()
            messages.success(request, "Keyword has been added successfully.")
            response = redirect("allnews")
            response['Location'] += '?option=country'
            return response
        else:
            messages.error(request, form.errors)
    else:
        form = KeywordForm()
        userkeywords = Keywords.objects.filter(user=request.user).values('keyword', 'created')
        return render(request, "NewsFeed/addkeyword.html", {"keyword_form": form, 'userkeywords': userkeywords})


def generatetoken(request):
    token = Token.objects.get_or_create(user=request.user)
    usertoken = token
    return render(request, "NewsFeed/generatetoken.html",
                  {'usertoken': usertoken})
