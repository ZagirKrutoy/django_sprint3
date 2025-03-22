from django.utils.timezone import now
from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.shortcuts import get_object_or_404


class IndexListView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    queryset = Post.objects.filter(
        pub_date__lte=now(),
        is_published__exact=True,
        category__is_published=True,
    ).order_by('-pub_date')[:5]


'''def index(request):
    template_name = "blog/index.html"
    inverted_posts = list(reversed(posts))
    return render(request, template_name, {"posts": inverted_posts})'''


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=now(),
            is_published=True,
            category__is_published=True
        )


'''def post_detail(request, id):
    template_name = "blog/detail.html"
    post = next((post for post in posts if post["id"] == id), None)

    return render(request, template_name, {"post": post})'''


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True)
        return Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=now()
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True)
        return context


'''def category_posts(request, category_slug):
    template_name = "blog/category.html"
    return render(request, template_name, {"category": category_slug})'''
