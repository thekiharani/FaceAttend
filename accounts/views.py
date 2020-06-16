# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect

from .forms import CustomUserCreationForm

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_instructor:
        # user is an admin
        return redirect('attendance:lessons')
    else:
        return redirect('attendance:my_courses')

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
