from django.conf import settings
import requests
import json
import random
from NewsFeed.models import Countries
from Newsapi.models import NewsItem


def schedule_api():
    allcountries = Countries.objects.all().values_list('countryName', flat=True)
    allnews = NewsItem.objects.all().values_list('title', flat=True)
    insertedlist = []
    # NewsItem.objects.all().delete()
    for country in allcountries:
        api_url = "https://newsapi.org/v2/top-headlines?country=" + country + "&category=business&apiKey=870fc67670de409b8243be8052873a8e"
        r = requests.get(api_url)
        if r.status_code == 200:
            articles = r.json()["articles"]
            for article in articles:
                if article['title'] not in allnews:
                    print(article['title'])
                    insertedlist.append(
                        NewsItem.objects.create(title=article['title'], source=article['source']['name'],
                                                url=article['url'], imageurl=article['urlToImage'], country=country))

    try:
        NewsItem.objects.bulk_create(insertedlist, batch_size=None, ignore_conflicts=False)
    except:
        pass
