from django.shortcuts import render
import requests

# Create your views here.
from django.http import HttpResponse

def getapinews(request):
    option=request.GET['option']
    if option == 'country':
        r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=870fc67670de409b8243be8052873a8e', params=request.GET)
    elif option == 'source':
        r = requests.get('https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=870fc67670de409b8243be8052873a8e', params=request.GET)
    if r.status_code == 200:   
        result = r.json()
        titles = []
        for news_item in result['articles']:
            titles.append(news_item['title'])

        return render(request,
                      'NewsFeed/news.html',{'titles': titles})

    return HttpResponse('Could not find data')