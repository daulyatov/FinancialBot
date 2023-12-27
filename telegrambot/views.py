from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import TelegramUser, TelegramIncome, TelegramExpense, TelegramSupport, TelegramAnswers
from .serializers import (
    TelegramUserSerializer,
    TelegramIncomeSerializer,
    TelegramExpenseSerializer,
    TelegramSupportSerializer,
    TelegramAnswersSerializer,
)


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['username']
   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TelegramIncomeViewSet(viewsets.ModelViewSet):
    queryset = TelegramIncome.objects.all()
    serializer_class = TelegramIncomeSerializer

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['user']
   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TelegramExpenseViewSet(viewsets.ModelViewSet):
    queryset = TelegramExpense.objects.all()
    serializer_class = TelegramExpenseSerializer

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['user']
   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TelegramSupportViewSet(viewsets.ModelViewSet):
    queryset = TelegramSupport.objects.all()
    serializer_class = TelegramSupportSerializer

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['user']
   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TelegramAnswersViewSet(viewsets.ModelViewSet):
    queryset = TelegramAnswers.objects.all()
    serializer_class = TelegramAnswersSerializer

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['user']
   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)