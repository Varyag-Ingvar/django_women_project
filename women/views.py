from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.generic import ListView

from .forms import AddPostForm
from .models import Women, Category

# меню на страницах сайта
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


class WomenHome(ListView):
    """вместо функции index сделаем класс WomenHome для отображения домашней страницы
    на базе класса ListView используемый для отображения списков (др.классы представлений см.документацию)"""
    model = Women  # используемая модель
    template_name = 'women/index.html'  # указываем какой шаблон использовать
    context_object_name = 'posts'  # имя объекта который передается в шаблон index.html в виде {% for post in posts %}

    def get_context_data(self, *, object_list=None, **kwargs):
        """формирует и статический и динамический контекст, который передается в шаблон.
         Сначала берем из базового класса ListView уже сформированный контекст,
         с помощью super().get_context_data(**kwargs)
        чтобы не переопределить уже существующие переменные выше - template_name, context_object_name и т.д. и т.п."""
        context = super().get_context_data(**kwargs)
        context['menu'] = menu  # добавляем к сформированному контексту еще данные, в данном случае передаем наше menu
        context['title'] = 'Главная страница'  # и заголовок страницы в браузере (имя вкладки)
        context['cat_selected'] = 0   # делаем чтобы категории отобр.другим цветом на странице при их выборе
        return context

    def get_queryset(self):
        """позволяет выбирать из таблицы Women нужные данныею.
        В данном случае возьмем записи, у которых параметр is_published=True"""
        return Women.objects.filter(is_published=True)


# def index(request):
#     """функция представления index отвечает за отображение шаблона index.html по маршруту с именем home"""
#     posts = Women.objects.all()   # выбираем из таблицы Women в БД все записи и сохраняем в переменную posts
#
#     """можем убрать переменную cats и исключить ее из коллекции context, т.к. мы заменили этот функционал
#     с помощью создания тегов для шаблонов в women/templatetags/women_tags.py с целью исключения дублирования кода
#     в функциях-представлениях, дабы не нарушать принцип DRY (переменная оставлена тут для наглядности)"""
#     cats = Category.objects.all()  # выбираем из таблицы Category в БД все записи и сохраняем в переменную cats
#
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)


def about(request):
    """функция представления about отвечает за отображение шаблона about.html по маршруту с именем about"""
    context = {'menu': menu, 'title': 'О сайте'}
    return render(request, 'women/about.html', context=context)


def addpage(request):
    """функция представления addpage отвечает за отображение шаблона addpage.html по маршруту с именем addpage"""
    if request.method == 'POST':  # если пользователь ввел в форму данные и нажал кнопку "добавить"
        form = AddPostForm(request.POST, request.FILES)  # добавляем форму, с заполненными пользователем данными.
        # !!!собязательно передаем вторым аргументом request.FILES !!! если хотим загрузить файлы (фото, в нашем случае)
        if form.is_valid():   # если данные введенные пользователем валидны, они идут в form.cleaned_data
            # try:
                # Women.objects.create(**form.cleaned_data)  # добавляем данные формы в БД
            form.save()   # добавляем данные формы в БД, только с вызовом метода save у form (women/forms.py)
                # такой вариант предпочтительнее, т.к. джанго автоматом генерирует исключения
                # при неверном заполнении формы, т.е. мы можем убрать блок try-except
            return redirect('home')     # и если добавление в БД успешно, то редирект на домашнюю страницу
            # except:
            #     form.add_error(None, 'Ошибка добавления статьи')  # если добавление в БД не прошло, выкинем исключение
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

