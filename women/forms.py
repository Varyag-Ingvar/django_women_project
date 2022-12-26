"""файл для создания форм"""

from django import forms
from .models import *


class AddPostForm(forms.Form):
    """Класс отображения формы для шаблона addpage.html
    Аттрибуты данного класса - это поля которые будут отображаться для заполнения в форме.
    К каждому полю можно применить стили с помощью параметра widget= (см.документацию джанго)"""
    title = forms.CharField(max_length=255, label='Заголовок')  # заголовок поста (параметр label отображает название поля на странице)
    slug = forms.SlugField(max_length=255, label='Слаг')  # слаг поста
    content = forms.CharField(label='Текст статьи', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))  # сам текст поста
    is_published = forms.BooleanField(label='Опубликована/нет', required=False)  # чекбокс - пост опубликован/не опубликован
    cat = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all())  # позволит выбирать категорию из списка

