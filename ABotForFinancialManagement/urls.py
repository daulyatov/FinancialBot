from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from telegrambot.views import TelegramUserViewSet, TelegramIncomeViewSet, TelegramExpenseViewSet,TelegramSupportViewSet, TelegramAnswersViewSet


router = routers.DefaultRouter()
router.register(r'user', TelegramUserViewSet)
router.register(r'income', TelegramIncomeViewSet)
router.register(r'expense', TelegramExpenseViewSet)
router.register(r'support', TelegramSupportViewSet)
router.register(r'answer', TelegramAnswersViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]


