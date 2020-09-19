# django_audio_recorder
# Create Django basic template

**Create virtual environmnet**  

python -m venv venv  
cd venv  
cd Scripts  
activate  
cd ..  
cd ..  
**Install django**  
pip install django  
**Create app**  
django-admin startproject main_app  
**Run Server**    
cd main_app  
python manage.py runserver  
**migrations**  
python manage.py migrate  
**create admin user**  
python manage.py createsuperuser   
now set your username and password here  
**Now create first app**  
python manage.py startapp sub_app  

**Register this sub_app to main_app**  
Go to settings of main_app and in INSTALLED_APPS ass sub_app as follows  
```  
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sub_app',
]
```
**create urls**  
create urls.py inside sub_app  
attach urls.py of subapp to urls.py of main app, write following code in main app urls.py  
go to main_app url.py  
``` 
from django.contrib import admin
from django.urls import path,include
from sub_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sub_app.urls'))
]
```

now go to urls.py of sub_app and add following  
```
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home')
    ]
```
inside view.py
```
def home(request):
	context={'print':'ok'}
	return render(request,'home.html',context)
```


**create a template**  
create a folder templates inside sub_app and inside the templates folder create home.html  
and write 
{{ print }}
**RUN app** 
Now run `python manage.py runserver` and you will every thing ok on browser  

# Work on templates
Now we will create some pages and added it to url as we did with home page  
First of all we create a base page  
```
header
{% block content %}

{% endblock %}
footer
```
in home page
{% extends 'base.html' %}
{% block content %}
{{ print }}
{% endblock %}

add to load static files
```
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
```
Every thing written before and after this block will be displayed on all pages
 Copy the starter page from boost strap and paste it in home page
Inside body tag, i pasted
```
 <div class='container'>
      <br><br>
   <form action="{% url 'home' %}" method="POST">
   {% csrf_token %}
    <label for="fname">Name:</label><br>
    <input type="text" id="fname" name="Name" value=""><br>
    <label for="email">Email:</label><br>
    <input type="email" id="email" name="email" value=""><br><br>
    <input type="submit" value="Submit">
  </form> 
</div>
```
We will put `action= "{% url 'home' %}"` the path in action is connected with `name='home'` in `urls.py`
Next we add `method="POST"` in our form. 
Dont forget to add csrf token

**Get these value in views.py**  
Next we need to fetch the values posted in form in views.py , so that we can further process them
```
def home(request):
	if request.method=='POST':
		name=request.POST['Name']
		mail=request.POST['email']
	return render(request,'home.html',{'print':name})
```
# Work on models  
Now we have to create model so that we can store data in database
Add the variables created in from in model, so that data from form can go through these models and store in database
```
class Upload(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField(max_length=50)
```
Following lines display the name in admin area, place it in class created above
```
	def __str__(self):
		return self.name
 ```
 **Migrate models**   
 run 
 ```
 python manage.py makemigrations
 python manage.py migrate
 ```
 
 **register the model**
 ```
 from .models import *
 admin.site.register(Upload)
 ```
 This will register the upload model to the admin area  
**save the values in home function at views.py**
```
def home(request):
	if request.method=='POST':
		name=request.POST['Name'] #here Name is from form name
		email=request.POST['email']#here email is from form email name
		submit =Upload(name=name,email=email)
		submit.save()
```
**Fetch the data stored**  
Now create an other page, which can fetch the data by searching
First create a page search.html in templates folder.    
Add a simple forum here
```
<form method='POST' action ="{% url 'search' %}">
{% csrf_token %}
  <label for="search">Search:</label><br>
  <input type="text" id="search" name="Search"><br>
  <button type="submit" value='Submit'>Submit</button>	
</form>
```

Add the page to urls.py of sub_app  
`path('search/',views.search,name='search')`
Once the page is added, create a  `search` function in `views.py` file
```
def search(request):
	if request.method=='POST':
		query=request.POST.get('Search')
		data=Upload.objects.filter(name__icontains=query)
		return render(request,'search.html',{'query_key':data})
	else:
		pass
	return render(request,'search.html',{'query_key':'Search Value'})

```
Write this `query_key` key in `search.html`  
and paste following
```
Name   |   Email 
<br>
{% for q in print %}
{{ q.name }}    | {{q.email}}
<br>
{% endfor %}
```
# Host it to heroku

**add static and media path**
```
MEDIA_ROOT = os.path.join(BASE_DIR, 'sub_app','media')   
MEDIA_URL = '/media/'  

STATIC_URL = '/static/'  
STATIC_ROOT = os.path.join(BASE_DIR, 'sub_app','static') 
```
**white noise**
`pip install whitenoise`
```
MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
 ```
``` STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'```

**add static file url**
add path of static files in main_app urls.py 
```
from django.views.static import serve
from django.conf import settings
from django.urls import path,include,re_path

re_path(r'^media/(?P<path>.*)$', serve, kwargs={'document_root': settings.MEDIA_ROOT})  
```
**create procfile**  
create Procfile  
`web: gunicorn main_app.wsgi:application --log-file -`  

**install gunicorn**  
`pip install gunicorn`  

**requirement**  
`pip freeze > requirements.txt`  
**runtime.txt**
`python-3.7.6`

* ALLOWED_HOSTS = ['*']


**hero dashboard**  
* create new app
* got to settings
* click on Config Vars
** add secret key there from settings file without ''
* create a file .env in main_app and add secret key there with ''
* add following line instead of secret key  
`pip install django-environ`
```
import environ
import os
environ.Env.read_env()
SECRET_KEY = os.environ['SECRET_KEY']
```
* now go to resources of app in heroku and add postgres
`pip install psycopg2`
* `pip install dj-database-url`
* add these lines below your databse  
`import dj_database_url`   
`DATABASES['default'] = dj_database_url.config(conn_max_age=600)`
* now go to heroku dashboard deploy and click on connect to github and search your app and press deploy  
* our site is ready now. But when we enter values, we will get an error. As we have to configure postgres database
**error**
```
ProgrammingError at /
relation "sub_app_upload" does not exist
LINE 1: INSERT INTO "sub_app_upload" ("name", "email") VALUES
```
go to heroku dashboard deploy click on Heroku Postgres, an other tab open and we see that there are no rows and no tables
* go to run console in heroku dashboard and run 
`python manage.py migrate`
now when we visit Heroku Postgres, we can see table there  
* now create superuser there, run this command in heroku console  
`python manage.py createsuperuser`

# Add javascript functionality
create a static folder inside sub_app and put your js file there  
in header of html add `{% load static %}`  
in body add  `<script src="{% static 'app.js' %}"></script>`
