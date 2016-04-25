from django.conf.urls import include, url
from django.contrib import admin

from django_tutorial.posts.views import get_all_posts, add_new_post, get_post_by_pk

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^posts/add/', add_new_post),
    url(r'^posts/(?P<pk>[0-9]+)/', get_post_by_pk),
    url(r'^posts/', get_all_posts),
]
