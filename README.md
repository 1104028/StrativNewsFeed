# StrativNewsFeed
Newsfeed Portal
Personalized News Feed

#Features

1. User Authentication implemented
2. Newsfeed based on user preferences. User can select multiple countries and sources.
3. Pagination added in news index
4. Scrape news in short time after news published in preference countries and sources
5. Send Email if any key preferred keywords appers in newsfeed
6. Newsfeed api for other app integration

License:	MIT
Versions
Python 3.10
Django 3.2.9

How to Install
#Prerequisite
Before starting the project, please install the necessary Library from requirements.txt
If you are a windows user, Please use this comman
pip install requirements.txt

# Run the stacks
python manage.py runserver
# Migrate database
django python manage.py migrate
# Create superuser
python manage.py createsuperuser
Initial Data of countries and sources provided from admin from admin panel
and for the News data Scheduler will run every 10 minutes. We don’t want the user to wait more than 15 minutes to get the updates headlines
Create Periodic task by registering StrativNewsFeed.JobScheduler.jobupdater.updater task and other options
http://localhost:8000/ in local
Settings
Set necessary keys and settings in these files
1. StrativNewsFeed.settings.py
2. JobScheduler.JobScheduler.py
apikey=<newsapi-api-key>
EMAIL_HOST_USER=<from-email-address>
EMAIL_HOST_PASSWORD=<emailpassword or key>
anymail.backends.sendgrid.EmailBackend
# Country and Source Seetings
Please login to admin site and add countries and sources as admin choice. Which will show in user settings panel.

#Basic Commands
Setting Up Your Users
To create a normal user account, just go to Sign Up and fill out the form. Once you submit it, if you provide valid user information, you will redirected to login page and ready to go.
Then, yoi will see the settings option, please set country and source. Also, if you need please set the keyword. 
Based on the settings, you will see the all news in index page.
To create an superuser account, use this command:

$ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

API
Before accessing API, Please login to you account and generate a api key from settings panel. 
Then try For api,check http://localhost:8000/api/status in local
We'll add api docs in later.

Deployment
The following details how to deploy this application.
