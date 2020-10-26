from . import views
from django.urls import path

app_name = 'index'

urlpatterns = [
    # /index/
    path('', views.index, name='index'),
    # /index/about-us/
    path('about-us/', views.about_us, name='about_us'),
    path('user-api/', views.user_api, name='api-access'),
]
