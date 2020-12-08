from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')  # где signup — это параметр "name" в path()
    template_name = 'registration/signup.html'


