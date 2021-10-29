import django.contrib.auth.views as auth
from django.urls import path
from .views import register, edit_profile,change_password


urlpatterns = [
    path('login/',auth.LoginView.as_view(template_name='auth/login.html',redirect_authenticated_user=True),name='login'),
    path('register/',register,name='register'),
    path('logout/',auth.LogoutView.as_view(template_name='auth/logout.html'),name='logout'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('profile/password/change/',change_password,name='profile-change-password'),
    path('password/reset/request/', auth.PasswordResetView.as_view(template_name='auth/reset_request.html'), name='passsword-reset'),
    path('password/reset/request/done/', auth.PasswordResetDoneView.as_view(template_name='auth/reset_done.html'), name='password-reset-done'),
    path('password/reset/confirm/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(template_name='auth/reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', auth.PasswordResetCompleteView.as_view(template_name='auth/reset_complete.html'), name='password-reset-complete')
]

