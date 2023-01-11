"""файл для создания форм на сайте"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class AddPostForm(forms.ModelForm):
    """Наследование от forms.ModelForm позволяет использовать в форме поля из конкретной модели приложения"""
    class Meta:
        model = Women   # выбираем модель, поля которой будут отображаться в форме
        # fields = '__all__'   # выбираем все поля модели
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']   # или передаем нужные поля модели в виде списка
        # с помощью widgets задаем нужным полям нужные стили, которые лежат в women/static/women/css/styles.css
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),    # задаем стили заголовку
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),  # задаем стили полю для ввода статьи
            'slug': forms.TextInput(attrs={'class': 'form-input'})      # задаем стили полю слаг (URL)
        }


# class AddPostForm(forms.Form):
#     """Класс отображения формы для шаблона addpage.html
#     Аттрибуты данного класса - это поля которые будут отображаться для заполнения в форме.
#     К каждому полю можно применить стили с помощью параметра widget= (см.документацию джанго)"""
#     title = forms.CharField(max_length=255, label='Заголовок')  # заголовок поста (параметр label отображает название поля на странице)
#     slug = forms.SlugField(max_length=255, label='Слаг')  # слаг поста
#     content = forms.CharField(label='Текст статьи', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))  # сам текст поста
#     is_published = forms.BooleanField(label='Опубликована/нет', required=False)  # чекбокс - пост опубликован/не опубликован
#     cat = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all())  # позволит выбирать категорию из списка




class RegisterUserForm(UserCreationForm):
    """класс формы регистрации пользователей, наследуемся от встроенного в джанго класса UserCreationForm
    Переопределим аттрибуты и зададим стили"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User   # стандартная модель юзера из джанго - импортируем выше, таблица в БД - auth_user
        fields = ('username', 'email', 'password1', 'password2')   # названия полей можно глянуть в админке (F12 - код элемента формы)
        # с помощью widgets задаем нужным полям нужные стили, которые лежат в women/static/women/css/styles.css
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),    # задаем стили из styles.css
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),  # задаем стили
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'})      # задаем стили
        # }


