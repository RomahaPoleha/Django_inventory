
from django.db import models
from django.contrib.auth.models import User



"""Таблица в БД для хранения Материнских плат и плат питания"""
class Consumable(models.Model):
    model = models.CharField("Модель", max_length=100, blank=True)
    name = models.CharField("Имя", max_length=100)
    modification = models.CharField("Модификация", max_length=10, blank=True)
    quantity = models.PositiveIntegerField("Количество")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField("Картинка", upload_to='consumables/', blank=True, null=True)


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
        verbose_name="Запросил",
        related_name='created_requests'
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
    issued_by= models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,blank=True,
                                 related_name='handled_requests' )
    class Meta:
        verbose_name="Оборудовние" # Задаёт человекочитаемое название модели в единственном числе(админка)
        verbose_name_plural="Запросы на выдачу" #Задаёт человекочитаемое название модели в единственном числе(админка)

class Issue(models.Model):
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE, verbose_name="Расходник")
    issued_to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получил")
    quantity = models.PositiveIntegerField("Количество")
    issued_at = models.DateTimeField("Выдан", auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues_made', verbose_name="Кто выдал")

    def __str__(self):
        return f"{self.quantity} шт. '{self.consumable.name}' выдано {self.issued_to.username}"

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ['-issued_at']  # новые выдачи сверху