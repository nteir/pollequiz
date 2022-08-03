from django.contrib import admin
from .models import QuizTake, QuizTakeLog

# Register your models here.
admin.site.register(QuizTake)
admin.site.register(QuizTakeLog)
