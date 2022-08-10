from django.urls import path
from pollequiz.run.views import views, auth_views


app_name = 'run'
urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('<int:quiz_id>/', views.TakeFirstPage.as_view(), name='quiz_start'),
    path('<int:quiz_id>/<int:pk>/<int:q_id>', views.TakeQuestion.as_view(), name='quiz_take'),
    path('result/<int:pk>/', views.QuizResult.as_view(), name='quiz_result'),
    path('takes/<int:quiz_id>/', auth_views.ResultsListForAuthors.as_view(), name='takes_list'),
    path('takes/detail/<int:pk>/', auth_views.ResultsForAuthors.as_view(), name='takes_detail'),
]
