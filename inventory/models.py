from django.db import models
#pip install Pillow


"""Таблица в БД для хранения Материнских плат и плат питания"""
class Consumable(models.Model):#Объявляется новый класс Consumable, который наследуется от models.Model. Это означает, что Consumable — это модель Django
    model=models.CharField("Модель",max_length=100)
    name=models.CharField("Имя",max_length=100) #Поле name CharField - текстовое поле ограниченной длины
    modification=models.CharField("Модификация",max_length=10) #То-же самое полу, смотреть выше
    quantity=models.PositiveIntegerField("Количество") #  поле с числом. PositiveIntegerField — целое число, которое может быть только нулём или положительным.
    description=models.TextField(blank=True,null=True) # TextField для хранения длинного текста без ограничения длины.
    image=models.ImageField("Картинка",upload_to='consumables/', # media/consumables/
                            blank=True,
                            null=True)


    def __str__(self):
        return f"{self.name} {self.modification}{self.quantity}" #Возвращает строковое представление модели(в админке отоброжает в привычном для человека виде)

    class Meta:
        verbose_name="Расходник" # Задаёт человекочитаемое название модели в единственном числе(админка)
        verbose_name_plural="Расходники" #Задаёт человекочитаемое название модели в единственном числе(админка)
