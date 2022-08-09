from django.urls import path
from pollequiz.api import views


app_name = 'api'
urlpatterns = [
    path('', views.QuizListAPIView.as_view(), name='quiz_list'),
    path('<int:pk>/', views.QuizAPIView.as_view(), name='quiz_detail'),
    path('full/<int:pk>/', views.FullQuizAPIView.as_view(), name='quiz_full'),
]
