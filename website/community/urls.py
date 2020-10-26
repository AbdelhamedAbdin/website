from . import views
from django.urls import path, re_path
from . import context_processors

app_name = 'community'

urlpatterns = [
    path('', views.UserQuestions.as_view(), name='user_questions'),
    path('ask-question/', views.UserAskingView.as_view(), name='user_asking'),
    path('ask-question/question-view/<slug:user_slug>/', views.QuestionDetail.as_view(), name='question_view'),
    path('delete-post/<slug:user_slug>/', views.DeletePost.as_view(), name="delete_post"),
    path('update-post/<slug:user_slug>/', views.UpdatePost.as_view(), name="update_post"),
    path('delete-comment/<int:pk>/', views.DeleteComment.as_view(), name="delete_comment"),
    path('update-comment/<int:pk>/', views.UpdateComment.as_view(), name="update_comment"),
    path('like/<slug:user_slug>/', views.LikePost.as_view(), name="like"),
    path('dislike/<slug:user_slug>/', views.DisLikePost.as_view(), name="dislike"),
    path('like-comment/<int:pk>/', views.LikeComment.as_view(), name="like_comment"),
    path('favourite/<slug:user_slug>/', views.AddFavorite.as_view(), name="favourite"),
    path('read_inbox/<int:id>/', context_processors.inbox_read_view, name='inbox_read_view'),
    path('all_items/', views.Inboxes.as_view(), name='all_items'),
    path('mark-all-as-read/', context_processors.mark_all_as_read, name='mark_all'),
    path('remove-all-notifications/', context_processors.remove_all_notifications, name='remove_all'),
    path('remove-notification/<int:id>/', context_processors.remove_notify, name='remove_notify'),
]
