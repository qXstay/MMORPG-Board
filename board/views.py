import logging
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Response, Category
from .forms import PostForm, ResponseForm
from .filters import ResponseFilter
from notifications.tasks import send_response_accepted_notification
from notifications.tasks import send_response_notification
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'board/index.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Post.CATEGORY_CHOICES
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            raise PermissionDenied
        return post


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['pk'])
        response = form.save()


        # Добавьте явный редирект
        return redirect('post_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/response_list.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Response.objects.filter(post__author=self.request.user)


        status = self.request.GET.get('status')
        if status == 'accepted':
            queryset = queryset.filter(accepted=True)
        elif status == 'pending':
            queryset = queryset.filter(accepted=False)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', 'all')
        return context

class OwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


def accept_response(request, pk):
    response = get_object_or_404(Response, id=pk)
    if request.user != response.post.author:
        raise PermissionDenied

    response.accepted = True
    response.save()

    return redirect('response_list')

def delete_response(request, pk):
    response = get_object_or_404(Response, id=pk)
    if request.user == response.post.author or request.user == response.author:
        response.delete()
    return redirect('response_list')
