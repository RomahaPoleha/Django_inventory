from django.shortcuts import render, redirect, get_object_or_404 # render отображает шаблон, redirect -перенаправляет после Post
from datetime import datetime
from .models import Consumable, Request,Fasteners,Issue
from .forms import ConsumableForm, FastenersForm, QuantityForm
from django.contrib import messages #Система flash-сообщений: «Выдано!», «Ошибка!».
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test #user_passes_test - встроенный декоратор Django для проверки произвольного условия на пользователе.
from urllib.parse import unquote

#История для пользователей
def history(request):
    history_list = Issue.objects.filter(
        issued_to=request.user
    ).order_by('-issued_at')

    return render(request, 'inventory/history.html', {
        'history_list': history_list
    })

# История для админа
@login_required
def history_admin(request):
    if not request.user.is_staff:
        return redirect('section_selection')  # или 403

    history_list = Issue.objects.all().order_by('-issued_at')  # все выдачи, не только текущего юзера

    return render(request, 'inventory/history.html', {
        'history_list': history_list
    })

#Домашняя страница с выводом данных из таблицы (Consumable)
def consumable_list(request): #принимающее объект request (HTTP-запрос от пользователя).
    query = request.GET.get('q', '').strip() # Получает значение параметра q из GET-запроса
    if query: # Проверяет, ввёл ли пользователь непустой поисковый запрос.
        consumables = Consumable.objects.filter( #Выполняет поиск по нескольким полям
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(modification__icontains=query)
        ).order_by('name')
    else:
        consumables = Consumable.objects.all().order_by('name') # Если запрос пустой — загружает все расходники, отсортированные по имени.

    #Пагинация 5 записей на страницу
    paginator=Paginator(consumables,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context={
        'page_obj':page_obj,
        'query':query,
        "current_date":datetime.now().strftime("%d.%m.%Y")}
    return render(request, "inventory/consumable_list.html",context) #Возвращает HTTP-ответ, рендеря шаблон inventory/consumable_list.html с переданным контекстом.

#Главная страница таблицы "Платы" (Consumable)
def section_selection(request):
    return render(request,"inventory/section_selection.html") #Рендеринг = превращение шаблона + данных → в готовую HTML-страницу.

# Добавление наименование в Consumable
@login_required
def add_consumable(request):
    if request.method =='POST':# Проверяет, был ли запрос отправлен методом POST (то есть пользователь нажал кнопку «Отправить» в форме).
        form=ConsumableForm(request.POST)  # Создаёт экземпляр формы ConsumableForm, заполняя её данными из POST-запроса (request.POST).
        if form.is_valid(): # Проверяет, корректны ли данные в форме
            form.save() # Сохраняет данные формы как новую запись в базе данных
            messages.success(request, f"Расходник  успешно добавлен!") #всплывающее уведомление об успехе
            return redirect('consumables_list') #Перенапровляем на главную (что-бы избежать повторной отправки формы
        else:
            messages.error(request,"Пожалуйста исправьте ошибки в форме.") #Если форма не корректна, показывает ошибку в форме
    else:
        form=ConsumableForm()

    return render(request, 'inventory/add_consumable.html',{'form':form})

@login_required
#Функция для редактирования данных в таблице "Платы" (Consumable)
def edit_consumable(request,pk): #pk — первичный ключ (id) редактируемого объекта, переданный из URL
    consumable=get_object_or_404(Consumable,pk=pk) #Пытается найти в базе данных объект Consumable с указанным pk(Если не найден — автоматически возвращает ошибку 404)
    if request.method=="POST":
        form =ConsumableForm(request.POST,instance=consumable) # instance=consumable — говорит Django: «не создавай новый объект, а обнови этот»
        if form.is_valid():
            messages.success(request, f"Расходник {consumable.name} успешно обновлён!")
            form.save() # Сохраняет изменения в базу данных (обновляет существующую запись).
            return redirect("consumables_list")
        else:
            messages.error(request,"Не удалось сохранить изменения. Проверьте данные.") # Если форма некорректна, показывает сообщение об ошибке. Пользователь останется на странице редактирования, и форма отобразится с ошибками.
    else:
        form =ConsumableForm(instance=consumable)
    return render(request,'inventory/edit_consumable.html', {'form': form, 'consumable': consumable})

#Функция для удаления из таблицы Платы (Consumable)
@login_required
def delete_consumable(request,pk):
    consumable=get_object_or_404(Consumable,pk=pk)
    if request.method=="POST":
        name=consumable.name
        consumable.delete()
        messages.success(request, f"Расходник {name} успешно удалён!")
        return redirect("consumables_list")
    return render(request,'inventory/delete_consumable.html', {'consumable': consumable})

# Запрос на выдачу из таблицы "Платы" (Consumable)
@login_required
def create_request(request, consumable_id):
    consumable = get_object_or_404(Consumable, id=consumable_id)
    if request.method == "POST":
        form = QuantityForm(request.POST)  # ← новая форма
        if form.is_valid():
            Request.objects.create(
                consumable=consumable,
                requested_by=request.user,
                quantity=form.cleaned_data['quantity'],
                status='pending'
            )
            messages.success(request, f"Запрос на '{consumable.name}' отправлен!")
        else:
            messages.error(request, "Ошибка: укажите корректное количество.")
        next_url = request.GET.get('next')
        return redirect(unquote(next_url)) if next_url else redirect('consumables_list')
    return redirect('consumables_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def issue_requests(request):
    pending_requests = Request.objects.filter(status='pending').select_related(
        'consumable', 'fastener', 'requested_by'
    ).order_by('-created_at')
    return render(request, 'inventory/issue_requests.html', {
        'pending_requests': pending_requests
    })

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def issue_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    # Защита от повторной обработки
    if req.status != 'pending':
        messages.warning(request, 'Этот запрос уже обработан.')
        return redirect('issue_requests')

    # Определяем, с каким типом мы работаем
    item = req.consumable or req.fastener  # ← Получаем НЕ None объект

    if request.method == "GET":
        return render(request, 'inventory/confirm_issue.html', {"issue": req, "item": item})

    if request.method == "POST":
        # Проверка остатка
        if item.quantity < req.quantity:
            messages.error(request, f"Недостаточно остатка! Доступно: {item.quantity}")
            return redirect('issue_requests')

        # Списываем количество
        item.quantity -= req.quantity
        item.save()

        # Создаём запись в истории (Issue)
        Issue.objects.create(
            consumable=req.consumable,  # будет None, если крепёж
            fastener=req.fastener,      # будет None, если плата
            issued_to=req.requested_by,
            quantity=req.quantity,
            issued_by=request.user
        )

        # Обновляем статус запроса
        req.status = 'issued'
        req.issued_by = request.user
        req.save()

        messages.success(request, f'Выдано: {req.quantity} шт. "{item.name}"')
        return redirect('issue_requests')



#Добавить новые данные в таблицу Крепёж (Fasteners)
@login_required
def add_fastener(request):
    if request.method =='POST':# Проверяет, был ли запрос отправлен методом POST (то есть пользователь нажал кнопку «Отправить» в форме).
        form=FastenersForm(request.POST)  # Создаёт экземпляр формы ConsumableForm, заполняя её данными из POST-запроса (request.POST).
        if form.is_valid(): # Проверяет, корректны ли данные в форме
            form.save() # Сохраняет данные формы как новую запись в базе данных
            messages.success(request, f"Расходник  успешно добавлен!") #всплывающее уведомление об успехе
            return redirect('fasteners_list') #Перенапровляем на главную (что-бы избежать повторной отправки формы
        else:
            messages.error(request,"Пожалуйста исправьте ошибки в форме.") #Если форма не корректна, показывает ошибку в форме
    else:
        form=FastenersForm()

    return render(request, 'inventory/add_fasteners.html',{'form':form})

#Функция для редактирования данных в таблице "Крепёж" (Fasteners)
@login_required
def edit_fastener(request,pk):
    fastener=get_object_or_404(Fasteners,pk=pk)
    if request.method=="POST":
        form=FastenersForm(request.POST,instance=fastener)
        if form.is_valid():
            messages.success(request,f"Расходник для 'Крепежа' {fastener.name} Успешно обновлён")
            form.save()
            return redirect("fasteners_list")
        else:
            messages.error(request,"Не удалось сохранить изменения. Проверьте данные")
    else:
        form=FastenersForm(instance=fastener)
    return render(request,'inventory/edit_fasteners.html', {'form':form,'fastener':fastener})


# Функция для удаления данных из таблицы "Крепёж" (Fasteners)
@login_required
def delete_fastener(request,pk):
    fastener=get_object_or_404(Fasteners,pk=pk)
    if request.method=="POST":
        name = fastener.name
        fastener.delete()
        messages.success(request, f"Расходник {name} успешно удалён")
        return redirect("fasteners_list")
    return render(request,'inventory/delete_fasteners.html',{'fastener':fastener})

#Вывод содержимого из таблицы "Крепёж" (Fasteners)
@login_required
def fasteners(request):
    query = request.GET.get('q', '').strip()
    if query:
        items = Fasteners.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('name')
    else:
        items = Fasteners.objects.all().order_by('name')

    context = {
        'items': items,  # Передаём список как 'items'
        'query': query,
        "current_date": datetime.now().strftime("%d.%m.%Y")
    }
    return render(request, "inventory/fastener_list.html", context)




@login_required
def create_request_fasteners(request, pk):
    fastener = get_object_or_404(Fasteners, pk=pk)
    if request.method == "POST":
        form = QuantityForm(request.POST)  # ← та же форма!
        if form.is_valid():
            Request.objects.create(
                fastener=fastener,
                requested_by=request.user,
                quantity=form.cleaned_data['quantity'],
                status='pending'
            )
            messages.success(request, f"Запрос на крепёж '{fastener.name}' отправлен!")
        else:
            messages.error(request, "Ошибка: укажите корректное количество.")
        next_url = request.GET.get('next')
        return redirect(unquote(next_url)) if next_url else redirect('fasteners_list')
    return redirect('fasteners_list')