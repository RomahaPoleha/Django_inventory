from . import views # из текущей директории испортируем views
from django.urls import path
from .views import ConsumableListAPIView,IssueListAPIView

urlpatterns=[
    path('delete_manufacturing/<int:pk>/',views.delete_manufacturing,name='delete_manufacturing'),
    path("add_manufacturing/",views.add_manufacturing, name='add_manufacturing'),
    path("edit_request_manufacturing/<int:pk>/",views.edit_manufacturing, name='edit_manufacturing'),
    path("manufacturing_list/", views.manufacturing_list, name="manufacturing_list"),
    path('api/history/', IssueListAPIView.as_view(), name='issue-list-api'),
    path('create_request/<int:consumable_id>/', views.create_request, name='create_request'),
    path('create_request_fasteners/<int:pk>/', views.create_request_fasteners, name='create_request_fasteners'),
    path('fasteners/', views.fasteners, name="fasteners_list"),
    path('history_admin' , views.history_admin, name='history_admin'), # путь вывода всех историй пользователей, который видит только админ
    path('history/',views.history,name='history'), # путь для выводы индивидуальных историй
    path("",views.section_selection,name="section_selection"), # путь главной страницы с выбором разделов
    path('consumables/',views.consumable_list,name='consumables_list'), # путь для вывода содержимоо таблицы Consumable
    path("add/",views.add_consumable, name='add_consumable'), # путь для добавления содержимоо в таблицу Consumable
    path('edit_fasteners/<int:pk>/',views.edit_fastener,name='edit_fasteners'),
    path('delete_fasteners/<int:pk>/',views.delete_fastener,name='delete_fasteners'),
    path('edit/<int:pk>/', views.edit_consumable, name='edit_consumable'),
    path('delete/<int:pk>/', views.delete_consumable, name='delete_consumable'),
    path('requests/',views.issue_requests,name='issue_requests'),
    path('issue/<int:request_id>/', views.issue_request, name='issue_request'),
    path('add_fasteners/',views.add_fastener,name="add_fasteners"),
    path('api/consumables/', ConsumableListAPIView.as_view(), name='consumable-list-api'),# Путь для вывода всех расходников в JSON списке

]