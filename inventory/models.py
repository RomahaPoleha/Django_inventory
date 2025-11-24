
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



"""Таблица в БД для хранения Материнских плат и плат питания"""
class Consumable(models.Model):
    model = models.CharField("Модель", max_length=100, blank=True)
    name = models.CharField("Имя", max_length=100)
    modification = models.CharField("Модификация", max_length=10, blank=True)
    quantity = models.PositiveIntegerField("Количество")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField("Картинка", upload_to='consumables/', blank=True, null=True)


    def __str__(self):
        return f"{self.name} {self.modification} {self.quantity}" #Возвращает строковое представление модели(в админке отоброжает в привычном для человека виде)

    class Meta:
        verbose_name="Запчасть для ремонта" # Задаёт человекочитаемое название модели в единственном числе(админка)
        verbose_name_plural="Запчасти для ремонта" #Задаёт человекочитаемое название модели в единственном числе(админка)

"""Таблица для храннения всего Крепежа"""
class Fasteners(models.Model):
    name=models.CharField("Наименование",max_length=100)
    quantity=models.PositiveIntegerField("Количество")
    min_quantity=models.PositiveIntegerField("Минимальный остаток")
    link=models.URLField("Ссылка на закуп")
    image = models.ImageField("Картинка", upload_to='fasteners/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.quantity} {self.min_quantity}"

    class Meta:
        verbose_name = "Крепёж"
        verbose_name_plural="Крепежи"


"""Определяем модель Django под названием Request, которая будет представлять таблицу в базе данных c выдаными расходниками"""
class Request(models.Model):
    # Поле внешнего ключа: связывает текущую запись с моделью Consumable.
    # При удалении связанного объекта Consumable запись в Request также будет удалена (CASCADE).
    # verbose_name задаёт человекочитаемое имя поля для админки и форм.
    consumable = models.ForeignKey(Consumable,on_delete=models.CASCADE, null=True,blank=True,verbose_name="Платы")
    fastener=models.ForeignKey(Fasteners,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Крепёж")
    # Поле внешнего ключа: связывает запрос с пользователем (модель User из django.contrib.auth).
    # При удалении пользователя все его запросы также удаляются.
    requested_by = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Запросил",related_name='requests_created')

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
                                 related_name='requests_handled' )
    def clean(self):
        if not(bool(self.consumable) ^bool(self.fastener)): # это XOR: True только если ровно одно значение истинно.
            raise ValidationError("Запрос должен ссылаться либо на плату, либо на крепёж, но не на оба сразу и не на ничего.")

    def get_item(self):
        return self.consumable or self.fastener

    class Meta:
        verbose_name="Оборудовние" # Задаёт человекочитаемое название модели в единственном числе(админка)
        verbose_name_plural="Запросы на выдачу" #Задаёт человекочитаемое название модели в единственном числе(админка)
        ordering=['-created_at']

"""Модель таблицы в которой храняться выданные расходники"""
class Issue(models.Model):
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE,null=True,blank=True, verbose_name="Платы")
    fastener = models.ForeignKey(Fasteners, on_delete=models.CASCADE,null=True,blank=True)
    issued_to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получил")
    quantity = models.PositiveIntegerField("Количество")
    issued_at = models.DateTimeField("Выдан", auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues_made_by_user', verbose_name="Кто выдал")

    def clean(self):
        if not(bool(self.consumable) ^bool(self.fastener)): # это XOR: True только если ровно одно значение истинно.
            raise ValidationError("Выдача должна ссылаться либо на плату, либо на крепёж.")

    def get_item(self):
        return self.consumable or self.fastener

    def __str__(self):
        return f"{self.quantity} шт. '{self.consumable.name}' выдано {self.issued_to.username}"

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ['-issued_at']  # новые выдачи сверху



