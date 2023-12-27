from rest_framework import serializers
from .models import TelegramUser, TelegramIncome, TelegramExpense, TelegramSupport, TelegramAnswers


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'
        
        
        
class TelegramIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramIncome
        fields = '__all__'
        

class TelegramExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramExpense
        fields = '__all__'
        
        
class TelegramSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramSupport
        fields = '__all__'
        
 
class TelegramAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramAnswers
        fields = '__all__'
        