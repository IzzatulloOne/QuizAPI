from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

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
        
    def update(self, instance, validate_data):
        instance.title = validate_data['title', instance.title]
        instance.save()

        answers_data = validate_data.pop('answers')
        new_answers_ids = []
        for answer_data in answers_data:
            try:
                answer = Answer.objects.get(pk=answers_data.id)
                answer.title = answer_data['title']
                answer.is_correct = answer_data['is_correct']
                new_answers_ids.append(id)
                answer.save()

            except Answer.DoesNotExist:
                new_answer =Answer.objects.create(
                    title=answer_data["title"],
                    is_correct=answer_data["is_correct"],
                    question=instance
                )
                new_answers_ids.append(new_answer.id)

        instance.answers.exclude(id__in=new_answers_ids).delete()        



class TestSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'nomi', 'creator', 'questions']

    def create(self, validated_data):
        question_data = validated_data.pop('questions')
        test = Test.objects.create(**validated_data)

        for question in question_data:
            questions_serializer = QuestionSerializer(data=question, many=True)
            questions_serializer.is_valid(raise_exception=True)
            questions_serializer.save(test=test)
        return test



class SelectedAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')
    answer_id = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), source='answer')
    correct_answer_title = serializers.CharField(read_only=True)
    is_correct = serializers.BooleanField(read_only=True)
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    answer = serializers.PrimaryKeyRelatedField(read_only=True)



class SubmissionSerializer(serializers.ModelSerializer):
    selected_answers = SelectedAnswerSerializer(many=True)
    correct_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    # test = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())
    
    def create(self, validated_data):
        test = validated_data.pop('test')
        user = validated_data.pop('user')

        submission = Submission.objects.create(test=test, user=user)

        count = 0

        correct_answer_title = ""
        correct_answer_list = question.answers.filter(is_correct=True)

        if correct_answer_list.exists():
            correct_answer_title = correct_answer_list.first().title
        for selected_answer in validated_data["selected_answers"]:
            question = selected_answer['question']
            answer = selected_answer['answer']
            is_correct = answer.is_correct

            SelectedAnswer.objects.create(
                **selected_answer,
                question=question,
                answer=answer,
                submission=submission,
                is_correct=is_correct,
                correct_answer_title=correct_answer_title
            )

            if is_correct:
                count += 1

        submission.correct_count = count
        submission.save()

        return submission



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["accessToken"] = data.pop("access")
        data["refreshToken"] = data.pop("refresh")

        data["user"] = {
            'user_id':self.user.username,
            'user_username':self.user.username,
            'avatar_url':""
        }


        return data



class MyTestSerializers(serializers.ModelSerializer):
    savollar_soni = serializers.SerializerMethodField()
    submissionlar_soni = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ['id', 'nomi', 'created_at', 'savollar_soni','submissionlar_soni']
    
    def get_savollar_soni(self, attrs):
        return attrs.questions.count()
    
    def get_submissionlar_soni(self, attrs):
        return attrs.submissions.count() 
    


class MySubmissionsList(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    correct_count = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'test', 'test_name', 'correct_count', 'total_count', 'created_at']

    
    def get_correct_count(self, obj):
        return obj.selected_answers.filter(is_correct=True).count()
    
    def get_total_count(self, obj):
        return obj.selected_answers.count()
    
    def get_test_name(self, obj):
        return obj.test.nomi
    

class SelectedAnswerFullSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')
    answer_id = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), source='answer')
    correct_answer_title = serializers.CharField(read_only=True)
    is_correct = serializers.BooleanField(read_only=True)
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)



class SubmissionFullSerializer(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    correct_count = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()
    selected_answers = SelectedAnswerFullSerializer(many=True)

    class Meta:
        model = Submission
        fields = ['id', 'test', 'test_name', 'correct_count', 'total_count', 'created_at', 'selected_answers']

    def get_correct_count(self, obj):
        return obj.selected_answers.filter(is_correct=True).count()
    
    def get_total_count(self, obj):
        return obj.selected_answers.count() 
    
    def get_test_name(self, obj):
        return obj.test.nomi
    

