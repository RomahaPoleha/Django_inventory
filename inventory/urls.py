from . import views # из текущей директории испортируем views
from django.urls import path

urlpatterns=[
    path('create_request/<int:pk>/', views.create_request_fasteners, name='create_request_fasteners'),
    path('history_admin' , views.history_admin, name='history_admin'),
    path('history/',views.history,name='history'),
    path("",views.section_selection,name="section_selection"),
    path('consumables/',views.consumable_list,name='consumables_list'),
    path("add/",views.add_consumable, name='add_consumable'),
    path('edit_fasteners/<int:pk>/',views.edit_fastener,name='edit_fasteners'),# Подключение пути
    path('delete_fasteners/<int:pk>/',views.delete_fastener,name='delete_fasteners'),
    path('edit/<int:pk>/', views.edit_consumable, name='edit_consumable'),  # Подключение пути
    path('delete/<int:pk>/', views.delete_consumable, name='delete_consumable'), # Подключение пути
    path('create_request/<int:consumable_id>/', views.create_request, name='create_request'), # Подключение пути
    path('requests/',views.issue_requests,name='issue_requests'),
    path('issue/<int:request_id>/', views.issue_request, name='issue_request'),
    path('fasteners/', views.fasteners, name="fasteners_list"),
    path('add_fasteners/',views.add_fastener,name="add_fasteners"),
]