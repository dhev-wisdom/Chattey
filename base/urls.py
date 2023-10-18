from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/login/', views.logIn, name='login'),
    path('auth/logout/', views.logOut, name='logout'),
    path('auth/register/', views.register, name='register'),
    path('auth/password-reset/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('auth/password-reset-sent/', PasswordResetDoneView.as_view(template_name='base/reset-email-sent.html'), name='email-sent'),
    path('auth/reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='base/reset-password-confirm.html'), name='confirm-reset'),
    path('auth/reset-password-done/', PasswordResetCompleteView.as_view(template_name='base/reset-password-complete.html'), name='reset-complete'),
    path('create-group/', views.create_group, name='create-group'),
    path('group-chat/<int:id>/', views.group_chat, name="group-chat"),
    path('group-profile/<int:id>/', views.group_profile, name="group-profile"),
    path('user-profile/<int:id>/', views.user_profile, name="user-profile"),
    path('edit-group/<int:id>/', views.edit_group, name="edit-group"),
    path('delete-group/<int:id>/', views.delete_group, name="delete-group"),
    path('private-chat/<str:username>', views.pchat, name='pchat'),
    path('edit-message/<int:id>/', views.edit_message, name="edit-message"),
    path('delete-message/<int:id>/', views.delete_message, name="delete-message"),
]