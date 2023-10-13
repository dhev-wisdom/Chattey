from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/login/', views.logIn, name='login'),
    path('auth/logout/', views.logOut, name='logout'),
    path('auth/register/', views.register, name='register'),
    path('auth/password-reset/', views.reset_password, name='reset-password'),
    path('create-group/', views.create_group, name='create-group'),
    path('group-chat/<int:id>/', views.group_chat, name="group-chat"),
    path('edit-group/<int:id>/', views.edit_group, name="edit-group"),
    path('delete_group/<int:id>/', views.delete_group, name="delete-group"),
    path('private-chat/<str:username>', views.pchat, name='pchat'),
    
    # path('confirm_delete_group/<int:id>/', views.confirm_delete_group, name="confirm-delete-group"),
    # path('delete-user/<id:pk>'),
    # path('delete-room/<id:pk>/'),
    # path('/delete-message/<id:pk>/'),
    # path('/edit-message'),
]