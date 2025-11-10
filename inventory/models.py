from django.db import models
from django.contrib.auth.models import User



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


"""Определяем модель Django под названием Request, которая будет представлять таблицу в базе данных c выдаными расходниками"""
class Request(models.Model):
    # Поле внешнего ключа: связывает текущую запись с моделью Consumable.
    # При удалении связанного объекта Consumable запись в Request также будет удалена (CASCADE).
    # verbose_name задаёт человекочитаемое имя поля для админки и форм.
    consumable = models.ForeignKey(
        Consumable,
        on_delete=models.CASCADE,
        verbose_name="Расходник"
    )

    # Поле внешнего ключа: связывает запрос с пользователем (модель User из django.contrib.auth).
    # При удалении пользователя все его запросы также удаляются.
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Запросил"
    )

    # Поле для хранения количества запрошенного расходника.
    # PositiveIntegerField гарантирует, что значение будет целым и >= 0.
    quantity = models.PositiveIntegerField("Количество")

    # Поле даты и времени автоматически устанавливается при создании записи (auto_now_add=True).
    # Не изменяется при последующих обновлениях объекта.
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    status=models.CharField(
        max_length=20,
        choices=[('pending','Ожидает'),('issued','Выдано')],
        default='pending'
    )
