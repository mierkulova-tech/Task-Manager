from django.shortcuts import render, get_object_or_404
from .models import Post


def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html',{'posts':posts})

def post_page(request, slug):
    post = get_object_or_404(Post, slug=slug)  # ← так безопаснее
    return render(request, 'posts/post_page.html', {'post': post})
