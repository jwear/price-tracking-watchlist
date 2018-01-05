from django.shortcuts import render, redirect
from django.contrib.auth import views as auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views import View

from .forms import UserCreationFormWithEmail

class AccountLoginView(auth.LoginView):
    template_name = 'accounts/login.html'

class AccountLogoutView(auth.LogoutView):
    def get(self, request, *args, **kwargs):
        super(AccountLogoutView, self).get(request, *args, **kwargs)
        return redirect('accounts:login')

class AccountRegisterView(View):
    template_name = 'accounts/register.html'
    form_class = UserCreationFormWithEmail

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            model = form.save()
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
            )
            login(request, user)
            return redirect('watch:profile')
        else:
            return render (request, self.template_name, {'form': form})
