from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ReportViewSet

router = DefaultRouter()
router.register(r'reportes', ReportViewSet, basename='reportes')

urlpatterns = [
    path('', include(router.urls)),
]