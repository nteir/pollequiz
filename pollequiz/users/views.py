from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
import pollequiz.text_constants as txt

User = get_user_model()


# Create your views here.
class UserCreateView(CreateView):
    
    model = User
    form_class = SignUpForm
    template_name = "form.html"
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = txt.SIGNUP_TITLE
        context['button_text'] = txt.SIGNUP_BTN
        return context

    def form_valid(self, form):
        valid = super(UserCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class UserLoginView(LoginView):
    
    model = User
    form_class = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class UserLogoutView(LogoutView):

    next_page = reverse_lazy('home')
