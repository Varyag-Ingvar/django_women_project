from django.db import models
from django.urls import reverse


class Women(models.Model):
    """Создаем модель (таблицу в БД) Women"""
    # поле id создается автоматически, SQL-запросы можно посмотреть в консоли командой -
    # python manage.py sqlmigrate women 0001, где women - название приложения, 0001 - номер файла миграции.
    title = models.CharField(max_length=255, verbose_name='Заголовок')  # параметр verbose_name отображает название в админке
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', null=True)  # слаг
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Статус публикации')
    # поле для связи "один ко многим" с таблицей Category, к cat джанго автоматом добавит _id и поле будет cat_id
    # ссылаемся на модель Category и защищаем запись в таблице women от удаления, при удалении записи из Category
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def __str__(self):
        """при чтении записи, вместо ссылки на объект будет возвращать заголовок(title) записи"""
        return self.title

    def get_absolute_url(self):  # метод именно с таким названием позволяет отобразить кнопку в админке - view on site
        """метод формирует динамический маршрут к конкретной записи из БД по ее id (primary key - pk),
        у экзепляра класса Women берем параметр pk (self.pk)
        и динамически присваиваем его в маршрут (в параметр post_id),
        который находится в women/urls.py --> path('post/<int:post_id>/', show_post, name='post')
        Далее мы используем этот метод в шаблоне index.html для перехода по полученной динамической ссылке,
        при нажатии кнопки 'Читать пост'"""
        return reverse('post', kwargs={'post_slug': self.slug})  # переделали по слагу вместо id(pk)

    class Meta:
        """Специальный вложенный класс, который используется в админ-панели для настройки данной модели
        и управления ею"""
        verbose_name = 'Известные женщины'  # эти названия будут отображаться в админке
        verbose_name_plural = 'Известные женщины'
        ordering = ['time_create', 'title']   # сортируем записи в админке по времени создания и потом по заголовку


class Category(models.Model):
    """Создаем модель (таблицу в БД) Category"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', null=True)

    def __str__(self):
        """при чтении записи, вместо ссылки на объект будет возвращать имя (name) записи (Актрисы, Певицы и т.д.)"""
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        """Специальный вложенный класс, который используется в админ-панели для настройки данной модели
        и управления ею"""
        verbose_name = 'Категории'  # эти названия будут отображаться в админке
        verbose_name_plural = 'Категории'
        ordering = ['name']   # сортируем записи в админке по названию



