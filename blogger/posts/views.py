from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Post


def home(request):
    selected = request.GET.get('category')
    published = Post.objects.filter(is_published=True)
    posts = published.order_by('-published_at')

    if selected:
        posts = posts.filter(category=selected)

    categories = [
        {
            'value': value,
            'label': label,
            'icon': Post.ICONS[value],
            'count': published.filter(category=value).count(),
        }
        for value, label in Post.CATEGORIES
    ]

    context = {
        'posts': posts,
        'categories': categories,
        'selected': selected,
        'selected_label': dict(Post.CATEGORIES).get(selected),
        'total': published.count(),
    }
    return render(request, 'posts/home.html', context)


def add_post(request):
    if request.method == 'POST':
        post = Post(
            title=request.POST['title'],
            content=request.POST['content'],
            category=request.POST['category'],
            is_published='is_published' in request.POST,
        )
        post.save()
        return redirect('posts:home')

    return render(request, 'posts/add_post.html', {'categories': Post.CATEGORIES})


def toggle_theme(request):
    current = request.COOKIES.get('theme', 'light')
    theme = 'light' if current == 'dark' else 'dark'

    next_url = request.GET.get('next', '/')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = '/'

    response = redirect(next_url)
    response.set_cookie('theme', theme, max_age=60 * 60 * 24 * 365)
    return response
