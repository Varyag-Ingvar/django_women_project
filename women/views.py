from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
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
    return HttpResponse('Add topic')


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

