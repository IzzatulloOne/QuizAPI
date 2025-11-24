from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tests', views.TestModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tests/<int:test_id>/questions', views.QuestionListCreateAPI.as_view(), name='question-list-create'),
]