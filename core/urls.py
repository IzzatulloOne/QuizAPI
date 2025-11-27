from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('tests/<int:pk>/', views.TestModelDestroyView.as_view(), name='test-list-create'),
    path('tests/<int:test_pk>/submissions', views.SubmissionAPIView.as_view(), name='submissions-list-create'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
    path('auth/login', views.CustomTokenObtainPairView.as_view(), name='custom_login'),
    path('my-test/', views.MyTestListView.as_view(), name='my-test'),
    path('tests/<int:test_id>/questions', views.TestQuetionsListView.as_view(), name='get-test'),
    path('tests/questions/<int:pk>', views.TestQuestionDetailView.as_view(), name='get-test'),
    path('my-submissions/', views.MySubmissionsListView.as_view(), name='my-submissions')
]