from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView

from accounts.models import Account
from posts.forms import SearchForm, PostForm, ReviewForm
from posts.models import Post, Comment


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'products'
    paginate_by = 6
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class PostAddView(LoginRequiredMixin, CreateView):
    template_name = 'add.html'
    model = Post
    context_object_name = 'post'
    form_class = PostForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


User = get_user_model()


class MainView(ListView):
    template_name = 'main.html'
    model = Post
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(username__icontains=self.search_value) | Q(email__icontains=self.search_value) | Q(
                first_name__icontains=self.search_value) | Q(last_name__icontains=self.search_value)
            user = User.objects.filter(query).first()
            if user:
                queryset = queryset.filter(author=user)
            else:
                queryset = queryset.none()
        else:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        if username is not None:
            return get_user_model().objects.get(username=username)
        else:
            return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login'] = self.object.username
        context['avatar'] = self.object.avatar.url if self.object.avatar else None
        context['name'] = self.object.get_full_name()
        context['info'] = self.object.info
        context['posts'] = self.object.posts.order_by('-created_at')

        return context



def create_comment(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            post.comments_count += 1
            post.save()
            return redirect('main')
    else:
        form = ReviewForm()
    comments = Comment.objects.filter(post=post).order_by('pk')
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'post_detail.html', context)


class SubscribeView(UpdateView):
    model = Account
    fields = []

    def get_success_url(self):
        return reverse_lazy('main')

    def form_valid(self, form):
        if self.object != self.request.user:
            if self.request.user in self.object.subscriptions.all():
                self.object.subscriptions.remove(self.request.user)
            else:
                self.object.subscriptions.add(self.request.user)
        subscriber_count = self.object.subscriptions.count()
        form.instance.subscriber_count = subscriber_count
        return super().form_valid(form)
