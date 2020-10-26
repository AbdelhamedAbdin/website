from .forms import SignUp, ResetPassword, EditForm, UpdateAvatarForm, UpdateInfoForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import View, CreateView, UpdateView, DetailView
from django.contrib import messages


class PasswordReset(PasswordResetView, FormView):
    template_name = 'accounts/password_reset_view.html'
    email_template_name = 'accounts/reset_password_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    form_class = ResetPassword

    def get_success_url(self):
        return reverse_lazy('accounts:password_reset_done')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_mail = form.cleaned_data['email']
            user_mail = User.objects.get(email=user_mail)
            if user_mail.email:
                return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        post_form = self.request.POST
        if post_form:
            try:
                self.post(request)
            except User.DoesNotExist:
                messages.error(self.request, 'This User Does Not Exist')
                return redirect('accounts:password_reset')
        return super().dispatch(request, *args, **kwargs)


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    # Reset Your Password By G-mail Account
    def send_mail(self, request, **kwargs):
        subject = "Complete the modification of the password form"
        message = "please check here"
        send_mail(subject=subject,
                  message=message,
                  from_email=request.user.email,
                  recipient_list=[request.user.email],
                  fail_silently=False)
        return render(request, self.template_name)


# User registration
class Register(CreateView):
    template_name = 'accounts/register.html'
    form_class = SignUp
    success_url = reverse_lazy('accounts:login')


@method_decorator(login_required, name='dispatch')
# view profile page
class ViewProfile(UpdateView):
    queryset = UserProfile.objects.all()
    template_name = 'accounts/profile.html'
    form_class = UpdateInfoForm
    slug_field = 'slug'
    slug_url_kwarg = 'user_slug'

    def get_success_url(self):
        return reverse_lazy('accounts:view_profile', kwargs={'user_slug': self.request.user.userprofile.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_prof = UserProfile.objects.get(user=self.request.user)
        context['user_prof'] = user_prof
        context['get_favourite'] = User.objects.get(username=self.request.user.username).favorite.all()
        return context

    def form_valid(self, form):
        form.instance.user_slug = self.request.user.userprofile.slug
        self.object = form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
# Edit Your accounts form
class EditView(View):
    template_name = 'accounts/edit_profile.html'

    def get(self, *args, **kwargs):
        form = EditForm(instance=self.request.user)
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = EditForm(self.request.POST or None, instance=self.request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Info updated')
            return redirect('accounts:view_profile', self.request.user.userprofile.slug)
        context = {'form': form}
        messages.error(self.request, 'Please, check the form for errors')
        return render(self.request, self.template_name, context)


class UserImage(DetailView):
    queryset = UserProfile.objects.all()
    template_name = 'accounts/user-image.html'
    slug_field = 'slug'
    slug_url_kwarg = 'user_slug'


@method_decorator(login_required, name='dispatch')
# Update Avatar
class UpdateAvatar(UpdateView):
    queryset = UserProfile.objects.all()
    template_name = 'accounts/change-image.html'
    form_class = UpdateAvatarForm
    model = UserProfile
    slug_field = 'slug'
    slug_url_kwarg = 'user_slug'

    def get_success_url(self):
        try:
            request_user = UserProfile.objects.get(user=self.request.user)
            return reverse_lazy('accounts:view_profile', kwargs={'user_slug': request_user.slug})
        except:
            raise ValueError('Error')

@login_required
# Remove user
def remove_user(request, user_slug):
    if User.objects.filter(username=user_slug).exists():
        user_request = User.objects.get(username=user_slug)
        user_request.delete()
        messages.success(request, 'your accounts has removed successfully. create another one.', extra_tags='rm_account')
    return redirect('accounts:register')
