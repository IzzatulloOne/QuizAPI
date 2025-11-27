from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet    
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


from .models import Test, Question, Answer, Submission, SelectedAnswer
from .serializers import (
    TestSerializer,
    QuestionSerializer,
    AnswerSerializer,
    SubmissionSerializer,
    CustomTokenObtainPairSerializer,
    MyTestSerializers,
)


class TestModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class QuestionListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, test_id: int):
        try:
           test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
           return Response({"error": "Test not found."}, status=404)
        

        question_serializer = QuestionSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)
        question_serializer.save(test=test)

        return Response(question_serializer.data, status=201)
        
    

class SubmissionAPIView(generics.CreateAPIView):
    def post(self, request: Request, test_pk: int):
        try:
            test = Test.objects.get(id=test_pk)
        except Test.DoesNotExist:
            return Response({"error": "Test not found."}, status=404)
        
        serializer = SubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(test=test, user=request.user)

        return Response(serializer.data, status=201)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class MyTestListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyTestSerializers

    def get_queryset(self):
        return Test.objects.filter(creator=self.request.user)


class TestQuetionsListView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_test(self):
        try:
            return Test.objects.get(pk=self.kwargs["test_id"])
        except Test.DoesNotExist:
            raise NotFound(detail="Test not found")

    def get_queryset(self):
        test = self.get_test()
        return Question.objects.filter(test=test)
    
    def perform_create(self, serializer):
        test = self.get_test()
        print(test)
        serializer.save(test=test)


class TestQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()