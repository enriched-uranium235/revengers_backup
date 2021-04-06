from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from accounts import views as account_views
from django.contrib.auth import views as auth_views

from . import settings_common, settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView
         .as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='password-reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('register/', account_views.register, name='register-users'),
    path('', include('avengers.urls')),
    path('profile/', account_views.profile, name='profile'),
]

# 開発サーバーでメディアを配信できるようにする設定
urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)