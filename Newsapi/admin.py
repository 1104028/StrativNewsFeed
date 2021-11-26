from django.contrib import admin
from .models import NewsItem

class News(admin.ModelAdmin):
    list_display = ('title', 'source','url','imageurl','country')

admin.site.register(NewsItem,News)
