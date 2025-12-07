from django.contrib import admin
from .models import Test, Question, Answer, Submission, SelectedAnswer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Submission)
admin.site.register(SelectedAnswer)