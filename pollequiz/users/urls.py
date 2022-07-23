from django.urls import path
from pollequiz.users import views


app_name = 'users'
urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('create/', views.UserCreateView.as_view(), name='signup'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
