from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
import pollequiz.text_constants as txt
import pollequiz.pq_objects as pq_objects

User = get_user_model()


# Custom mixin for Users app
class SilentLoginMixin(ModelFormMixin):
    """
    Silently logs in user after sign up
    or user info update.
    """
    def form_valid(self, form):
        valid = super().form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


# Create your views here.
class UserCreateView(pq_objects.PQFormContextMixin, SilentLoginMixin, CreateView):

    model = User
    form_class = SignUpForm
    template_name = "form.html"
    success_url = reverse_lazy('home')
    title_text = txt.SIGNUP_TITLE
    btn_text = txt.SIGNUP_BTN

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super(UserCreateView, self).get(request, *args, **kwargs)


class UserUpdateView(
    LoginRequiredMixin,
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    SilentLoginMixin,
    UserPassesTestMixin,
    UpdateView
):

    model = User
    template_name = "form.html"
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    redirect_url = reverse_lazy('home')
    title_text = txt.UPDATE_USER_TITLE
    btn_text = txt.UPDATE_BTN

    def test_func(self):
        return self.request.user == self.get_object()


class UserLoginView(LoginView):

    model = User
    form_class = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class UserLogoutView(LogoutView):

    next_page = reverse_lazy('home')
