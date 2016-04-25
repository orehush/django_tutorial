from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http.response import HttpResponse
from django.core.context_processors import csrf

from django_tutorial.posts.models import Post
from django_tutorial.posts.forms import PostForm


def get_all_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        context = {'posts': posts}
        return render_to_response('posts/all_posts.html', context=context)


def get_post_by_pk(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render_to_response('posts/one_post.html', context=context)


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
