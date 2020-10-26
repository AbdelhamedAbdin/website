from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.CommunityListView.as_view(), name='ask-api-view'),
    path('<slug:ask_slug>/', views.CommunityDetailView.as_view(), name='question-detail'),
]
