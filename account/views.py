from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login


from .forms import RegisterForm


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm
    # success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')




