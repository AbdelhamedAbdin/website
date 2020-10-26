from django.urls import path
from . import views
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetCompleteView)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


app_name = 'accounts'


class LoginRedirect(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:view_profile', args=[self.request.user.userprofile.slug])

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'username or password are invalid. please try again.', extra_tags='validate_form')
        return redirect('accounts:login')


urlpatterns = [
    # /accounts/login/
    path('login/', LoginRedirect.as_view(), name='login'),
    # /accounts/logout/
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html', next_page=reverse_lazy('accounts:login')), name='logout'),
    # /accounts/register/
    path('register/', views.Register.as_view(), name='register'),
    # /accounts/view-profile/
    path('view-profile/<slug:user_slug>/', views.ViewProfile.as_view(), name='view_profile'),
    # /accounts/edit-profile/
    path('edit-profile/<slug:user_slug>/', views.EditView.as_view(), name='edit_profile'),
    # /accounts/password-change/
    path('password-reset/', views.PasswordReset.as_view(), name='password_reset'),
    # /accounts/password-change/done/
    path('password-reset-done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    # /accounts/password-copmlete/
    path('password-copmlete/', PasswordResetCompleteView.as_view(template_name='accounts/password_complete.html'),
         name='password_complete'),
    # /accounts/user-image/12/
    path('user-image/<slug:user_slug>/', views.UserImage.as_view(), name="user_image"),
    # /accounts/new-image/
    path('new-image/<slug:user_slug>/', views.UpdateAvatar.as_view(), name="add_avatar"),
    # /accounts/delete-user/medoabdin/
    path('delete-user/<slug:user_slug>/', views.remove_user, name="remove_user"),
]
