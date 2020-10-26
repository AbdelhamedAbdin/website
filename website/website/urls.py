from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
import notifications.urls

urlpatterns = [
    path('', include('index.urls')),
    path('accounts/', include('accounts.urls')),
    path('account/', include('allauth.urls')),
    path('community/', include('community.urls')),
    path('admin/', admin.site.urls),
    # Create an API View
    path('api/accounts/', include('accounts.api_accounts.urls')),
    path('api/community/', include('community.api.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

# initialize the environment to set Images
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # /accounts/password-reset-confirm/uidb64/token/
    path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                         success_url=reverse_lazy('accounts:password_complete')),
                                         name='password_reset_confirm'),
)
