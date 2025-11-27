from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tests', views.TestModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('tests/<int:test_id>/questions', views.QuestionListCreateAPI.as_view(), name='question-list-create'),
    path('tests/<int:test_pk>/submissions', views.SubmissionAPIView.as_view(), name='submissions-list-create'),
    path('auth/login', views.CustomTokenObtainPairView.as_view(), name='custom_login'),
    path('my-test/', views.MyTestListView.as_view(), name='my-test'),
    path('tests/<int:test_id>/questions', views.TestQuetionsListView.as_view(), name='get-test'),
    path('tests/questions/<int:pk>', views.TestQuestionDetailView.as_view(), name='get-test')
]