from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, profileUpdateForm
from django.contrib.auth.models import User
from blog.models import post
from django.conf import settings
# Create your views here.

def register(request):
    if request.method == 'POST':
      form = UserRegisterForm(request.POST)
      if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          messages.success(request, f'Your account has been created! You are now able to login')
          return redirect('login')
    else:
      form = UserRegisterForm()

    return render (request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    logged_in_user_posts = post.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'users/profile.html', {'posts': logged_in_user_posts})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render (request, 'users/edit_profile.html', context)

