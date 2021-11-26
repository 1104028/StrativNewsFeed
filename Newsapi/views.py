from django.views import View
from django.http import JsonResponse
from rest_framework import permissions
import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewsItem
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from NewsFeed.models import Countries, Sources, Keywords, Mapper


class ApiNews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request.user)
        userallcountries = Mapper.objects.filter(user=request.user, itemName="Country").values_list('selecteddata',
                                                                                                    flat=True)
        userallsources = Mapper.objects.filter(user=request.user, itemName="Source").values_list('selecteddata',
                                                                                                 flat=True)
        newsfinallist = []  # contails filtered news

        allnews = NewsItem.objects.all()

        if allnews.count() > 0:
            for news in allnews:
                if news.country in userallcountries:
                    if news.source in userallsources:
                        newsfinallist.append(news)
                        break
        items_data = []
        for item in newsfinallist:
            items_data.append({
                'title': item.title,
                'source': item.source,
                'url': item.url,
                'imageurl': item.imageurl,
                'country': item.country,
            })
        data = {
            'items': items_data,
            'count': len(newsfinallist),
        }

        return JsonResponse(data)


class StatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': "OK",
        }
        return Response(content)
