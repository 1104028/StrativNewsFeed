from django.contrib import admin
from .models import Countries,Sources,Keywords,Mapper

class Country(admin.ModelAdmin):
    list_display = ('countryName', 'created')

class Source(admin.ModelAdmin):
     list_display = ('sourceName', 'created')

class keyword(admin.ModelAdmin):
     list_display = ('keyword', 'created','user')

class MappingAdmin(admin.ModelAdmin):
    list_display = ('itemName', 'selecteddata', 'user')

admin.site.register(Countries,Country)
admin.site.register(Sources,Source)
admin.site.register(Keywords,keyword)
admin.site.register(Mapper,MappingAdmin)


