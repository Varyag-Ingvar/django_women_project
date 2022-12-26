from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound

from .forms import AddPostForm
from .models import Women, Category

# меню на страницах сайта
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    """функция представления index отвечает за отображение шаблона index.html по маршруту с именем home"""
    posts = Women.objects.all()   # выбираем из таблицы Women в БД все записи и сохраняем в переменную posts

    """можем убрать переменную cats и исключить ее из коллекции context, т.к. мы заменили этот функционал
    с помощью создания тегов для шаблонов в women/templatetags/women_tags.py с целью исключения дублирования кода
    в функциях-представлениях, дабы не нарушать принцип DRY (переменная оставлена тут для наглядности)"""
    cats = Category.objects.all()  # выбираем из таблицы Category в БД все записи и сохраняем в переменную cats

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Main page',
        'cat_selected': 0,
    }

    return render(request, 'women/index.html', context=context)


def about(request):
    """функция представления about отвечает за отображение шаблона about.html по маршруту с именем about"""
    context = {'menu': menu, 'title': 'О сайте'}
    return render(request, 'women/about.html', context=context)


def addpage(request):
    """функция представления addpage отвечает за отображение шаблона addpage.html по маршруту с именем addpage"""
    if request.method == 'POST':  # если пользователь ввел в форму данные и нажал кнопку "добавить"
        form = AddPostForm(request.POST)  # добавляем форму, с заполненными пользователем данными.
        if form.is_valid():   # если данные введенные пользователем валидны, они идут в form.cleaned_data
            try:
                Women.objects.create(**form.cleaned_data)  # добавляем данные формы в БД
                return redirect('home')     # и если добавление в БД успешно, то редирект на домашнюю страницу
            except:
                form.add_error(None, 'Ошибка добавления статьи')  # если добавление в БД не прошло, выкинем исключение
    else:
        form = AddPostForm()  # выводим пустую форму (настройки формы лежат в women/forms.py)

    context = {'form': form, 'menu': menu, 'title': 'Добавление статьи'}  # передаем форму в шаблон ('form': form)
    return render(request, 'women/addpage.html', context=context)


def contact(request):
    return HttpResponse('Feedback')


def login(request):
    return HttpResponse('Authorization')


def show_post(request, post_slug):
    """отображает отдельную статью при нажатии кноапки 'Читать пост' """
    post = get_object_or_404(Women, slug=post_slug)  # переделали по слагу вместо id(pk)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,  # ссылка на идентификатор категории объекта класса Women
    }

    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    posts = Women.objects.filter(cat__slug=cat_slug)  # выбираем из таблицы Women в БД записи соотв.тек.категории (cat_slug)
    cats = Category.objects.all()  # выбираем из таблицы Category в БД все записи и сохраняем в переменную cats

    if len(posts) == 0:  # если нет постов в соотвествующей категории, выводим исключение 404
        raise Http404()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Отображение по категориям',
        'cat_selected': cat_slug,
    }

    return render(request, 'women/index.html', context=context)


def page_not_found(request, exception):
    """Переопределяем поведение 404 ошибки, работает когда в settings проекта параметр DEBUG = False"""
    return HttpResponseNotFound('Страница не найдена')

