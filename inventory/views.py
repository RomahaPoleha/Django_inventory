from django.shortcuts import render #функция render автоматически ищет шаблоны в папках teamplates
from datetime import datetime


# Create your views here.
def home(request):
    context={"current_date":datetime.now().strftime("%d.%m.%Y")}
    return render(request, "inventory/home.html",context)

def about(request):
    return render(request,"inventory/about.html")