from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Test, Question, Answer, Submission, SelectedAnswer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'lastname', 'firstname']



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'is_correct']



class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'title', 'test' , 'answers']

    def create(self, validated_data):
        answers = validated_data.pop('answers')

        question = Question.objects.create(**validated_data)

        for answer_data in answers:
            Answer.objects.create(question=question, **answer_data)

        return question

    def validate_answers(self, answers):
        count = 0

        for answer in answers:
            if answer["is_correct"]:
                count += 1
            
            if count > 1:
                raise serializers.ValidationError("Only one answer can be correct.")
            return count == 1


class TestSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'nomi', 'creator', 'questions']


class SelectedAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')
    answer_id = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), source='answer')


class SubmissionSerializer(serializers.ModelSerializer):
    selected_answers = SelectedAnswerSerializer(many=True)
    
    def create(self, validated_data):
        test = validated_data.pop('test')
        user = validated_data.pop('user')

        submission = Submission.objects.create(test=test, user=user)

        for selected_answer in validated_data["selected_answers"]:
            question = selected_answer['question']
            answer = selected_answer['answer']
            is_correct = answer.is_correct

            SelectedAnswer.objects.create(
                question=question,
                answer=answer,
                submission=submission,
                is_correct=is_correct
            )

        return submission