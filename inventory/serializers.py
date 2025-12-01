from rest_framework import serializers
from.models import Consumable, Issue

"""Создание сериализатора между моделью и JSON"""
class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consumable
        fields =['id','name','quantity','description']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'consumable', 'issued_to', 'quantity', 'issued_at']