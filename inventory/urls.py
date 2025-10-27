from . import views # из текущей директории испортируем views
from django.urls import path

urlpatterns=[
    path("",views.home,name="home"),
    #путь к функции home() из файла views
    path("about/",views.about,name="about"),
    path("add/",views.add_consumable, name='add_consumable'),
]