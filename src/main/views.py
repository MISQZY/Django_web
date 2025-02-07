from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404

from .forms import UserLoginForm


def main_page(request):
    return render(request, 'base.html')

def user_login(request):
    form = UserLoginForm(request.POST or None)

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли!")
            return redirect('home')
        else:
            messages.error(request, "Ошибка входа. Проверьте правильность данных.")

    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.user == user or request.user.is_staff:
        return render(request, 'main/profile.html', {'user_profile': user})
    else:
        raise Http404("У вас недостаточно доступа для просмотра данной страницы")