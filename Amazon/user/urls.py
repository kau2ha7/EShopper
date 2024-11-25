from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='user/password_change.html'),name='password_change'),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name = 'user/password_change_done.html'),name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),name='password_reset'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
]
