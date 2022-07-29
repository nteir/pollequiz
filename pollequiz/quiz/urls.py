from django.urls import path
from pollequiz.quiz import views


app_name = 'quiz'
urlpatterns = [
    path('', views.quiz.QuizListView.as_view(), name='list_all'),
    path('my/', views.quiz.MyQuizListView.as_view(), name='list_my'),
    path('<int:quiz_id>/', views.question.QuestionsListView.as_view(), name='quiz_card'),
    path('new/', views.quiz.QuizCreateView.as_view(), name='new'),
    path('<int:pk>/edit/', views.quiz.QuizUpdateView.as_view(), name='quiz_update'),
    path('<int:pk>/delete/', views.quiz.QuizDeleteView.as_view(), name='quiz_delete'),
    path('<int:quiz_id>/new/', views.question.QuestionCreateView.as_view(), name='question_new'),
    path('<int:quiz_id>/<int:pk>/edit/', views.question.QuestionUpdateView.as_view(), name='question_update'),
    path('<int:quiz_id>/<int:pk>/delete/', views.question.QuestionDeleteView.as_view(), name='question_delete'),
]
