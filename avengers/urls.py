from django.urls import path

from . import views


app_name = 'avengers'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('diary_list/', views.DiaryListView.as_view(), name="diary_list"),
    path('diary-detail/<int:pk>/', views.DiaryDetailView.as_view(), name="diary_detail"),
    path('diary-create/', views.DiaryCreateView.as_view(), name="diary_create"),
    path('diary-update/<int:pk>/', views.DiaryUpdateView.as_view(), name="diary_update"),
    path('diary-delete/<int:pk>/', views.DiaryDeleteView.as_view(), name="diary_delete"),
    path('accuse_list/', views.AccuseListView.as_view(), name="accuse_list"),
    path('accuse_detail/<int:pk>/', views.AccuseDetailView.as_view(), name="accuse_detail"),
    path('community_room/', views.MessageView.as_view(), name="comment_list"),
    path('create_message/', views.MessageCreateView.as_view(), name="comment_create"),
    path('personal_comment/', views.PersonalMessageView.as_view(), name="your_comment"),
    path('message_detail/<int:pk>/', views.MessageDetailView.as_view(), name="message_detail"),
    path('comment_update/<int:pk>/', views.MessageUpdateView.as_view(), name="comment_update"),
    path('comment-delete/<int:pk>/', views.MessageDeleteView.as_view(), name="comment_delete"),
    path('comment/<int:post_pk>/', views.comment_create, name='comment_view'),
    path('reply/<int:comment_pk>/', views.reply_create, name='reply_create'),
]
