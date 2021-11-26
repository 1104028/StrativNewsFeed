from django.apps import AppConfig


class NewsapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Newsapi'

    def ready(self):
    	from JobScheduler import jobupdater
    	jobupdater.start()
