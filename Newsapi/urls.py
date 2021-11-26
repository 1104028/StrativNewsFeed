from django.urls import path, include
from .views import ApiNews, StatusView

urlpatterns = [
      path('allnews', ApiNews.as_view()),
      path('status', StatusView.as_view())
]