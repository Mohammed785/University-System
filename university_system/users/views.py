from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,ChangePasswordForm,MyInfoForm
from .decorators import check_login
#TODO add templates for pass reset and decorators for login view


@check_login
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Now You Can Login')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', context={'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = MyInfoForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'InfoUpdated')
    else:
        form = MyInfoForm(instance=request.user)
    return render(request,'users/edit_profile.html',context={'form':form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if request.user.check_password(form.data['old_password']) and form.is_valid():
            if form.data['new_password']==form.data['confirm_password']:
                request.user.set_password(form.data['new_password'])#TODO make it with is_valid() in forms
                request.user.save()
                messages.success(request,'Password Changed Success')
            else:
                messages.success(request,'Password Does not Match')
        else:
            messages.warning(request,'Your Old Password Is Wrong')
    else:
        form = ChangePasswordForm()
    return render(request,'users/change_password.html',context={'form':form})