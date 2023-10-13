from django.shortcuts import render, redirect
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from .registration_form import RegistrationForm
from .group_chat import GroupChatForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
        groups = ChatRoom.objects.filter(creator=request.user)
    else:
        groups = None
    context = {'users': regisetered_users, 'groups': groups}
    return render(request, 'base/home.html', context)

def pchat(request, username):
    other_user = User.objects.get(username=username)
    context ={'other_user': other_user}
    return render(request, 'base/pchat.html', context)

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

def group_chat(request, id):
    group = ChatRoom.objects.get(id=id)
    context = {'group': group}
    return render(request, 'base/group-chat.html', context)

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

def confirm_delete_group(request, id):
    group = ChatRoom.objects.get(id=id)
    context = {'group': group}
    return render(request, 'base/confirm-delete-room.html', context)

def delete_group(request, id):
    group = ChatRoom.objects.get(id=id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully')
        return redirect('home')
    context = {'group': group}
    return render(request, 'base/confirm-delete-room.html', context)
            
