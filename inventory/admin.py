from django.contrib import admin
from .models import Consumable

"""Подключение админки для отоброжения БД"""
@admin.register(Consumable) #Декоратор, который регистрирует модель Consumable в административной панели Django.
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('name','quantity','modification','description','image') # Указывает, какие поля модели отображать в виде столбцов(админка)
    list_filter = ('modification',) # Добавляет боковую панель фильтров в админке.
    search_fields = ('name','description') # Это включает поисковую строку в верхней части списка, позволяя искать записи по полям name и description.
    ordering = ('name',) # Задаёт стандартную сортировку записей в списке админки — по полю name по возрастанию.
