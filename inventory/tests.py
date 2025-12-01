from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Consumable, Request


class IssueRequestViewTest(TestCase):
    def setUp(self):
        # Создаём тестового админа и пользователя
        self.admin = User.objects.create_user(
            username='admin', password='adminpass', is_staff=True
        )
        self.user = User.objects.create_user(
            username='user', password='userpass'
        )
        # Создаём расходник
        self.consumable = Consumable.objects.create(
            name="Гость",
            quantity=10
        )
        # Создаём запрос
        self.request = Request.objects.create(
            consumable=self.consumable,
            requested_by=self.user,
            quantity=3,
            status='pending'
        )
        self.client = Client()

    def test_issue_request_decreases_quantity(self):
        # Логинимся под админом
        self.client.login(username='admin', password='adminpass')

        # Делаем POST-запрос на подтверждение выдачи
        url = reverse('issue_request', args=[self.request.id])
        response = self.client.post(url)

        # Проверяем: редирект на список запросов
        self.assertRedirects(response, reverse('issue_requests'))

        # Обновляем данные из БД
        self.consumable.refresh_from_db()
        self.request.refresh_from_db()

        # Проверяем: остаток уменьшился на 3
        self.assertEqual(self.consumable.quantity, 7)
        # Проверяем: статус запроса изменился
        self.assertEqual(self.request.status, 'issued')
