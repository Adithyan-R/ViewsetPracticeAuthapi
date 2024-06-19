from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import TutorialViewset, TutorialList , RegisterApi , LoginApi


router = DefaultRouter()
router.register(r'tutoriallist',TutorialList, basename='tutorialList'),
router.register(r'tutorialview',TutorialViewset, basename='tutorialDetail'),

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/',RegisterApi.as_view()),
    path('login/', LoginApi.as_view()),

]

