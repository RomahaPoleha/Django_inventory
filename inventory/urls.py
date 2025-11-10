from . import views # из текущей директории испортируем views
from django.urls import path

urlpatterns=[
    path("",views.home,name="home"),
    #путь к функции home() из файла views
    path("about/",views.about,name="about"),# Подключение пути
    path("add/",views.add_consumable, name='add_consumable'), # Подключение пути
    path('edit/<int:pk>/', views.edit_consumable, name='edit_consumable'),  # Подключение пути
    path('delete/<int:pk>/', views.delete_consumable, name='delete_consumable'), # Подключение пути
    path('create_request/<int:consumable_id>/', views.create_request, name='create_request'), # Подключение пути
    path('requests/',views.issue_requests,name='issue_requests'),
]