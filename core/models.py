from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Test(models.Model):
    nomi = models.CharField(max_length=33)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)



class Question(models.Model):
    title = models.CharField(max_length=1500)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)



class Answer(models.Model):
    title = models.CharField(max_length=355)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


    
class Submission(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class SelectedAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='selected_answers')
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)