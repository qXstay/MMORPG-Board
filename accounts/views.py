from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from allauth.account.views import SignupView, LoginView
from board.models import Post
from .forms import CustomSignupForm, ProfileForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from allauth.account.views import ConfirmEmailView

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def get_form_class(self):
        return CustomSignupForm


class CustomLoginView(LoginView):
    template_name = 'account/login.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_posts'] = Post.objects.filter(author=self.request.user)[:5]
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirm.html'