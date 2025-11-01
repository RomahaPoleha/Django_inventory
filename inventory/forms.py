from django import forms
from .models import Consumable

"""Форма для добавления"""
class ConsumableForm(forms.ModelForm):
    class Meta:
        model=Consumable #  Указывает, что эта форма основана на модели Consumable
        fields =["name","modification","quantity","description",'model'] # Определяет, какие поля модели должны быть включены в форму
        """class="form-control" — CSS-класс из Bootstrap, который делает поле стилизованным (скруглённые углы, отступы, адаптивность и т.д.)."""
        widgets={
            "description": forms.Textarea(attrs={"rows":3,"class":"form-control"}), #form-control  настраивают внешний вид полей.
            "name":forms.TextInput(attrs={'class':'form-control'}),
            'modification':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'model':forms.TextInput(attrs={'class':'form-control'})
        }