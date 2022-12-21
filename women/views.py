from django.shortcuts import render
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


def show_post(request, post_id):
    return HttpResponse(f'show topic with id = {post_id}')


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)  # выбираем из таблицы Women в БД записи соотв.тек.категории (cat_id)
    cats = Category.objects.all()  # выбираем из таблицы Category в БД все записи и сохраняем в переменную cats

    if len(posts) == 0:  # если нет постов в соотвествующей категории, выводим исключение 404
        raise Http404()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Отображение по категориям',
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=context)


def page_not_found(request, exception):
    """Переопределяем поведение 404 ошибки, работает когда в settings проекта параметр DEBUG = False"""
    return HttpResponseNotFound('Страница не найдена')

