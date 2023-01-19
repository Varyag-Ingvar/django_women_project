from django.contrib import admin

# Register your models here.

# импортируем модели для работы с ними в админ-панели
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    """класс котрый позволяет отобразить нужные поля модели Women в админке"""
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')  # поля отображаемые в админке
    list_display_links = ('id', 'title')  # поля, на которые мы можем кликнуть и перейти в соотв.статью
    search_fields = ('title', 'content')  # поля, по которым мы можем осуществлять поиск
    list_editable = ('is_published',)   # список полей котрые можно редактировать (передается кортеж!!!)
    list_filter = ('title', 'is_published', 'time_create')  # поля, по которым можно фильтровать статьи в админке
    prepopulated_fields = {'slug': ('title',)}  # в админке поле slug будет заполняться автоматом по полю title
    # fields - список полей отображаемых при редактировании поста
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # список нередактируемых полей - только для чтения

    def get_html_photo(self, object):
        """Отобразим в админке картинки постов вместо ссылок на них.
         mark_safe - импортируем, эта функция делает html-теги рабочими внутри python-строки
         передадим результат в параметр list_display выше - для отображения картинки вместо ссылки на нее
         (если картинка у поста есть, чтобы не было ошибки - реализуем проверку)"""
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "миниатюра фото"   # название поля с фоткой в админке



class CategoryAdmin(admin.ModelAdmin):
    """класс котрый позволяет отобразить нужные поля модели Category в админке"""
    list_display = ('id', 'name', 'slug')  # поля отображаемые в админке
    list_display_links = ('id', 'name')  # поля, на которые мы можем кликнуть и перейти в соотв.статью
    search_fields = ('name',)  # поля, по которым мы можем осуществлять поиск (кортеж! нужна запятая если один элемент)
    prepopulated_fields = {'slug': ('name',)}  # в админке поле slug будет заполняться автоматом по полю name


# регистрируем модели в админке (сначала саму модель, уже затем админ-класс)
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

# изменим заголовки в админке
admin.site.site_title = 'Админ-панель сайта'
admin.site.site_header = 'Админ-панель сайта об известных женщинах'
