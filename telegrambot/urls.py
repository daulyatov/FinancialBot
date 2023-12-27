from django.urls import path
from .views import (TelegramUserViewSet, TelegramIncomeViewSet, TelegramExpenseViewSet,
        TelegramSupportViewSet, TelegramAnswersViewSet)
from rest_framework.routers import DefaultRouter


urlpatterns = []

router = DefaultRouter()
router.register('api/user', TelegramUserViewSet, basename='user')
router.register('api/income', TelegramIncomeViewSet, basename='income')
router.register('api/expense', TelegramExpenseViewSet, basename='expense')
router.register('api/support', TelegramSupportViewSet, basename='support')
router.register('api/answer', TelegramAnswersViewSet, basename='answer')

urlpatterns += router.urls

