from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post


def published_posts_filter(post_objects):
    return post_objects.filter(pub_date__lte=timezone.now())


def select_related(post_objects):
    return post_objects.order_by('-pub_date')


def index(request):
    post_list = select_related(published_posts_filter(Post.objects))
    latest_post = post_list.first()
    other_posts = post_list.exclude(id=latest_post.id) if latest_post else post_list
    popular_posts = Post.objects.order_by('-views')[:5]

    return render(request, 'pages/index.html', {
        'latest_post': latest_post,
        'other_posts': other_posts,
        'popular_posts': popular_posts
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1
    post.save(update_fields=['views'])
    return render(request, 'pages/detail.html', {'post': post})
