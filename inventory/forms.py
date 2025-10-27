from django import forms
from .models import Consumable

class ConsumableForm(forms.ModelForm):
    class Meta:
        model=Consumable
        fields =["name","modification","quantity","description"]
        #widgets добавляют CSS-классы Bootstrap
        widgets={
            "description": forms.Textarea(attrs={"rows":3,"class":"form-control"}), #form-control  настраивают внешний вид полей.
            "name":forms.TextInput(attrs={'class':'form-control'}),
            'modification':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control','min':'0'})
        }