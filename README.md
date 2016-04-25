# tutorial_django
-----------------

## Environment:  
    Language: python3.4
    OS: Linux
    packages: virtualenvwrapper, python3-pip, 

## Step 0: Install packages:
```
sudo apt-get install virtualenvwrapper python3-pip
```

## Step 1: Create a work directory and virtualenv

Run in console commands: 
```
mkdir tutorial
cd tutorial
mkvirtualenv tutorial_env -p /usr/bin/python3
```
## Step 2: Install Django and create project

Run in console commands:
```
pip install django==1.8
django-admin.py startproject django_tutorial
```

## Step 3: Add new app to project

Run in console commands:
```
cd django_tutorial/django_tutorial
django-admin.py startapp posts
```

## Structure directories in django project:
```
django_tutorial
├-- django_tutorial # root directory
    ├-- posts # our app posts
        ├-- migrations # directory with migrations
            ├-- __init__.py
        ├-- __init__.py
        ├-- admin.py
        ├-- models.py
        ├-- tests.py
        ├-- views.py
    ├-- __init__.py
    ├-- settings.py
    ├-- urls.py
    ├-- wsgi.py
├-- db.sqlite3 # our database
├-- manage.py # file for project manage
```

Register our app in file settings.py in section INSTALLED_APPS

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_tutorial.posts',
)
```


## Step 4: Run server

Run in console command:
```
python manage.py runserver
```

Open in browser url: http://127.0.0.1:8000

## Step 5: Make first model

Write model Post in file posts/models.py

```python
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_lenght=255)
    text = models.TextField(max_length=2047)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
```

## Step 6: Run migrations

Run in console commands:
```
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Admin page

For manages records in db we needs to register our model in file posts/admin.py

```python
from django.contrib import admin
from django_tutorial.posts.models import Post

admin.site.register(Post)
```

For access to admin page we must have a superuser permission.
Run in console commands for create superuser:
```
python manage.py createsuperuser
```

Run server:
```
python manage.py runserver
```

Open in browser url 127.0.0.1:8000/admin/ and type you login and password created by previous command

## Step 8: Create view, router, template

I hope that you created a few posts in admin page. Next try to make handler on our url.

Add some code to file posts/views.py

```python
from django.shortcuts import render_to_response

from django_tutorial.posts.models import Post


def get_all_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        context = {'posts': posts}
        return render_to_response('posts/all_posts.html', context=context)
```

Next we must link url with handler function. Add this url 
```python
    url(r'^posts/', get_all_posts)
```

to file tutorial/urls.py

```python
from django.conf.urls import include, url
from django.contrib import admin

from django_tutorial.posts.views import get_all_posts

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^posts/', get_all_posts),
]
```

Next we must create a some template for show our data. 
Create directories `templates/posts` in directory posts and create html file with name `all_posts.html`.
For preview our data we use some django templates language.

Add next code to file templates/posts/all_posts.py

```html
{% for post in posts %}
    <div>
        <h1>Title: {{ post.title }} </h1> <br> <hr>
        <p>
            Text: {{ post.text }} <br>
            Author is: {{ post.author }} <br>
            Post was created: {{ post.created }} <br>
        </p>
    </div>
{% endfor %}
```

It`a all. Run server and open this url http://127.0.0.1:8000/posts/ in your browser.

# Step 9: View for preview post by pk

Create new template `templates/posts/one_post.html` for preview posts by pk.

Add next content to template:

```html
<div>
    <h1>Title: {{ post.title }} </h1> <br> <hr>
    <p>
        Text: {{ post.text }} <br>
        Author is: {{ post.author }} <br>
        Post was created: {{ post.created }} <br>
    </p>
</div>
```

Next we need to create view:

```python
from django.shortcuts import render_to_response, get_object_or_404

def get_post_by_pk(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render_to_response('posts/one_post.html', context=context)
```

And next add router for handling with using regex for recognizing pk:

```python
from django_tutorial.posts.views import get_post_by_pk

urlpatterns = [
    ...
    url(r'^posts/(?P<pk>[0-9]+)/', get_post_by_pk),
    url(r'^posts/', get_all_posts),
    ...
]
```


## Step 10: POST request for add new post to DB

For validation data request in POST we needs create a django form.
Add it in file `posts/forms.py`:

```python
from django import forms

from django_tutorial.posts.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', )
```

Next we need add view for handle GET request for render form and POST request for add post to db.
Add view to file `posts/views.py`

```python
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse

def add_new_post(request):
    context = csrf(request)
    if request.method == 'GET':
        context.update({'form': PostForm()})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid() and not request.user.is_anonymous():
            data = form.clean()
            data.update({'author': request.user})
            post = Post(**data)
            post.save()
            return redirect('/posts/{pk}/'.format(pk=post.id))
        context.update({'form': form})
        if request.user.is_anonymous():
            return HttpResponse(
                content='<h1>You are not authorized for adding post</h1>',
                status=401
            )
    return render_to_response('posts/add_new_post.html', context)
```

Next needs add a template for preview `(templates/posts/add_new_post.html)`:

```html
<form action="." method="post"> {% csrf_token %}
    {{ form.as_p }} <br>
    <input type="submit" value="New Post">
</form>
```

And linking view and url:

```python
from django_tutorial.posts.views import add_new_post

urlpatterns = [
    ...
    url(r'^posts/add/', add_new_post),
    ...
]
```


## Step 11: Create a head template with a common content for all templates

For example, `posts/templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
</head>
<body>

<header>
    <div class="head">
        <h1>It`s some app on Python/Django</h1>
    </div>
</header>
<div class="content">
    {% block content %}{% endblock %}
</div>
<footer>
    <div class="info">
        Here is some info like as common info in any footers.
    </div>    
</footer>
</body>
</html>
```

For extends in other templates add this string `{% extends 'base.html' %}` in each template.
And for overriding block content do next:

```html
{% extends 'base.html' %}

{% block content %}
... some content
{% endblock %}
```


## Step 11: Add static files like as js, css, images

Add next lines to settings.py

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'tutorial/static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_content"),
)
```

Create some css file and change template in your choice.
 
For example, add file `style.css` to dir static_content:

```css
.content {
    background: orange;
    margin: 50px auto;
    padding: 20px;
    width: 600px;
    height: 400px;
}

.head {
    text-align: center;
}

.info {
    text-align: center;
}
```

## What the next?

### We have a opportunity to deploy to the heroku: 
https://devcenter.heroku.com/articles/getting-started-with-python#introduction

### Read the django girl tutorial: 
http://tutorial.djangogirls.org/en/index.html

### Read the documentation django: 
https://docs.djangoproject.com/en/1.8/

### See to django packages and use their: 
https://www.djangopackages.com/
