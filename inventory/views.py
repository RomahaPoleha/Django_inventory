from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect #функция render автоматически ищет шаблоны в папках teamplates
from datetime import datetime
from .models import Consumable #Импорт модели
from .forms import ConsumableForm # Импортируем форму
from django.contrib import messages


# Create your views here.
def home(request):
    consumables= Consumable.objects.all().order_by('name') #Мы добавили .order_by('name'), чтобы расходники шли по алфавиту
    context={
        'consumables':consumables,
        "current_date":datetime.now().strftime("%d.%m.%Y")}
    return render(request, "inventory/home.html",context)

def about(request):
    return render(request,"inventory/about.html")

def add_consumable(request):

    if request.method =='POST':
        form=ConsumableForm(request.POST)
        if form.is_valid():
            messages.success(request,f"Расходник  успешно добавлен!")
            form.save()
            return redirect('home') #Перенапровляем на главную
    else:
        form=ConsumableForm()

    return render(request, 'inventory/add_consumable.html',{'form':form})

