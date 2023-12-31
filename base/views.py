from django.shortcuts import render, redirect
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .registration_form import RegistrationForm
from .group_chat import GroupChatForm
from .edit_message import EditMessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'base/password-reset.html'
    email_template_name = 'base/password-reset-email.html'
    subject_template_name = 'base/password-reset-subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('reset-complete')


def logIn(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
            return render(request, 'base/login.html')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and password does not match')
    return render(request, 'base/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Your registration was successful')
            return redirect('login')
        else:
            messages.error(request, "An error was encountered during registration")
            context = {'form': form, 'messages': messages}
            return render(request, 'base/register.html', context)
    else:
        form = RegistrationForm()
        context = {'form': form, 'messages': messages}
    return render(request, 'base/register.html', context)

def logOut(request):
    logout(request)
    return redirect('home')

def reset_password(request):
    return render(request, 'base/password-reset.html')

def home(request):
    regisetered_users = User.objects.all()
    if request.user.is_authenticated:
        groups = ChatRoom.objects.filter(participants=request.user)
    else:
        groups = None
    context = {'users': regisetered_users, 'groups': groups}
    return render(request, 'base/home.html', context)

@login_required(login_url="login")
def pchat(request, username):
    other_user = User.objects.get(username=username)
    if request.user.is_authenticated:
        chat_messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
        ).order_by('timestamp')
    else:
        chat_messages = None
    context ={'other_user': other_user, 'chat_messages': chat_messages}
    return render(request, 'base/pchat.html', context)

def delete_message(request, id):
    if request.user.is_authenticated:
        message = Message.objects.get(id=id)
        if message.room:
            room = message.room
        else:
            room = None
        if request.method == 'POST':
            message.delete()
            return redirect('pchat', message.receiver)
        context = {'message': message, 'room': room}
        return render(request, 'base/confirm-delete-message.html', context)
    
def edit_message(request, id):
    message = Message.objects.get(id=id)
    if message.room:
        room = message.room
    else:
        room = None
    if request.method == 'POST':
        form = EditMessageForm(request.POST, instance=message)
        if form.is_valid():
            message = form.save()
            return redirect('pchat', message.receiver)
    else:
        form = EditMessageForm(instance=message)
    context = {'form': form, 'message': message, 'room': room}
    return render(request, 'base/edit-message.html', context)

@login_required
def create_group(request):
    if (request.method == 'POST'):
        form = GroupChatForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.participants.add(request.user)
            participants = request.POST.getlist('participants')
            for participant_id in participants:
                participant = User.objects.get(id=participant_id)
                group.participants.add(participant)
            
            messages.success(request, 'Group chat created successfully')
            return redirect('group-chat', group.id)
        else:
            messages.error(request, 'An error was encountered before group chat could be successfully created')
    else:
        form = GroupChatForm()
    context = {'form': form}
    return render(request, 'base/create-room.html', context)

@login_required
def group_chat(request, id):
    group = ChatRoom.objects.get(id=id)
    group_messages = Message.objects.filter(room=group)
    context = {'group': group, 'group_messages': group_messages}
    return render(request, 'base/group-chat.html', context)

def group_profile(request, id):
    group = ChatRoom.objects.get(id=id)
    group_messages = Message.objects.filter(room=group)
    context = {'group': group, 'group_messages': group_messages}
    return render(request, 'base/group-profile.html', context)

def user_profile(request, id):
    user = User.objects.get(id=id)
    users = User.objects.all()
    groups = ChatRoom.objects.filter(participants=user)
    context = {'user': user, 'users': users, 'groups': groups}
    return render(request, 'base/user-profile.html', context)

@login_required
def edit_group(request, id):
    group = ChatRoom.objects.get(id=id)
    if request.method == 'POST':
        form = GroupChatForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            group.participants.add(request.user)
            messages.success(request, 'Group details updated successfully')
            return redirect('group-chat', group.id)
        else:
            messages.error(request, 'An error occured while editing group')
    else:
        form = GroupChatForm(instance=group)
    context = {'form': form, 'group': group}
    return render(request, 'base/edit-room.html', context)

@login_required
def confirm_delete_group(request, id):
    group = ChatRoom.objects.get(id=id)
    context = {'group': group}
    return render(request, 'base/confirm-delete-room.html', context)

@login_required
def delete_group(request, id):
    group = ChatRoom.objects.get(id=id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully')
        return redirect('home')
    context = {'group': group}
    return render(request, 'base/confirm-delete-room.html', context)
            
