from django import forms
from .models import Consumable,Request,Fasteners

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

class RequestForm(forms.ModelForm):
    class Meta:
        model=Request
        fields=['quantity']

        widgets={'quantity':forms.NumberInput(attrs={'class':'form-control','min':'1'})}

    def clean_quantity(self): #clean_quantity — это метод, который Django вызывает при валидации поля quantity
        quantity=self.cleaned_data['quantity']
        if quantity <=0:
            raise forms.VAlidationError("Количество должно быть больше нуля.")
        return quantity

class FastenersForm(forms.ModelForm):
    class Meta:
        model=Fasteners#  Указывает, что эта форма основана на модели Consumable
        fields =["name","quantity",'min_quantity','link','description' ] # Определяет, какие поля модели должны быть включены в форму
        """class="form-control" — CSS-класс из Bootstrap, который делает поле стилизованным (скруглённые углы, отступы, адаптивность и т.д.)."""
        widgets={
            "description": forms.Textarea(attrs={"rows":3,"class":"form-control"}), #form-control  настраивают внешний вид полей.
            "name":forms.TextInput(attrs={'class':'form-control'}),
            'min_quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'link':forms.TextInput(attrs={'class':'form-control'})
        }

