from django.urls import path
from . import views

app_name = 'api_accounts'

urlpatterns = [
    path('<slug:slug>/', views.UserProfileRetrieveView.as_view(), name="detail"),
]
