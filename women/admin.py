from django.contrib import admin

# Register your models here.

# импортируем модели для работы с ними в админ-панели
from .models import *


class WomenAdmin(admin.ModelAdmin):
    """класс котрый позволяет отобразить нужные поля модели Women в админке"""
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # поля отображаемые в админке
    list_display_links = ('id', 'title')  # поля, на которые мы можем кликнуть и перейти в соотв.статью
    search_fields = ('title', 'content')  # поля, по которым мы можем осуществлять поиск
    list_editable = ('is_published',)   # список полей котрые можно редактировать (передается кортеж!!!)
    list_filter = ('title', 'is_published', 'time_create')  # поля, по которым можно фильтровать статьи в админке
    prepopulated_fields = {'slug': ('title',)}  # в админке поле slug будет заполняться автоматом по полю title


class CategoryAdmin(admin.ModelAdmin):
    """класс котрый позволяет отобразить нужные поля модели Category в админке"""
    list_display = ('id', 'name', 'slug')  # поля отображаемые в админке
    list_display_links = ('id', 'name')  # поля, на которые мы можем кликнуть и перейти в соотв.статью
    search_fields = ('name',)  # поля, по которым мы можем осуществлять поиск (кортеж! нужна запятая если один элемент)
    prepopulated_fields = {'slug': ('name',)}  # в админке поле slug будет заполняться автоматом по полю name


# регистрируем модели в админке (сначала саму модель, уже затем админ-класс)
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
