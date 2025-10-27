from django.contrib import admin
from .models import Consumable

@admin.register(Consumable) #регистрирует модель.
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('name','quantity','modification','description') # какие поля показывать в списке.
    list_filter = ('modification',) # фильтр по модифифкации.
    search_filter = ('name','description') # поиск по названию и описанию.
    ordering = ('name',) # сортировка по имени.
