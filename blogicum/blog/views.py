from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count

from .models import Post, Category, Comment, User
from .forms import RegistrationForm, ProfileEditForm, CommentForm, PostForm


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location')
        .annotate(comment_count=Count('comments')),
        pk=post_id
    )

    if not post.is_published and post.author != request.user:
        return redirect('blog:index')

    if post.pub_date > timezone.now() and post.author != request.user:
        return redirect('blog:index')

    context = {
        'post': post,
        'form': CommentForm(),  # Переименовано из comment_form в form
        'comments': post.comments.all().order_by('created_at')
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.filter(
        pub_date__lte=timezone.now(),
        is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


@login_required
def profile(request, username):
    profile = get_object_or_404(User, username=username)  # Используем profile вместо profile_user
    post_list = profile.posts.select_related('category', 'location').annotate(
        comment_count=Count('comments')
    )
    
    if request.user != profile:
        post_list = post_list.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
    
    paginator = Paginator(post_list.order_by('-pub_date'), 10)
    return render(request, 'blog/profile.html', {
        'profile': profile,  # Используем profile как в шаблоне
        'page_obj': paginator.get_page(request.GET.get('page')),
        'user': request.user  # Добавляем user для проверки auth
    })


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:login')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user  # Редактируем только текущего пользователя

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )
