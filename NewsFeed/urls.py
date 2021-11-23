from django.urls import path, include
from . import views

urlpatterns = [
      path('allnews', views.getapinews, name='allnews'),
      path("register", views.registration, name="register"),
      path("login", views.userlogin, name="login"),
      path("logout", views.userlogout, name="logout")
]
