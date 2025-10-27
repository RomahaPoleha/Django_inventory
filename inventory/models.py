from django.db import models

# Create your models here.

class Consumable(models.Model):
    name=models.CharField("Имя",max_length=100)
    modification=models.CharField("Модификация")
    quantity=models.PositiveIntegerField("Количество")
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name} {self.modification}{self.quantity}"

    class Meta:
        verbose_name="Расходник"
        verbose_name_plural="Расходники"
