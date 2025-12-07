from django.contrib import admin
from .models import Test, Question, Answer, Submission, SelectedAnswer

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomi', 'creator', 'created_at')
    search_fields = ('nomi', 'creator__username')
    list_filter = ('created_at',)
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'text')
    search_fields = ('text', 'test__nomi')
    list_filter = ('test',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('question', 'is_correct')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'user', 'submitted_at')
    search_fields = ('test__nomi', 'user__username')
    list_filter = ('submitted_at',)

@admin.register(SelectedAnswer)
class SelectedAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'answer')
    search_fields = ('submission__user__username', 'answer__text')
    list_filter = ('submission',)