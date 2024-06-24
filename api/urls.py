from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import TutorialViewset, TutorialList, RegisterApi, LoginApi, CommentViewSet

router = DefaultRouter()
router.register(r'tutoriallist',TutorialList, basename='tutorialList'),
router.register(r'tutorialview',TutorialViewset, basename='tutorialDetail'),
router.register(r'comments',CommentViewSet, basename='comment'),


urlpatterns = [
    path('api/', include(router.urls)),
    path('register/',RegisterApi.as_view(),name='register'),
    path('login/', LoginApi.as_view(),name='login'),

]

