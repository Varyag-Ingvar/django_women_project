from django.db import models
from django.urls import reverse


class Women(models.Model):
    """Создаем модель (таблицу в БД) Women"""
    # поле id создается автоматически, SQL-запросы можно посмотреть в консоли командой -
    # python manage.py sqlmigrate women 0001, где women - название приложения, 0001 - номер файла миграции.
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    # поле для связи "один ко многим" с таблицей Category, к cat джанго автоматом добавит _id и поле будет cat_id
    # ссылаемся на модель Category и защищаем запись в таблице women от удаления, при удалении записи из Category
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        """при чтении записи, вместо ссылки на объект будет возвращать заголовок(title) записи"""
        return self.title

    def get_absolute_url(self):
        """метод формирует динамический маршрут к конкретной записи из БД по ее id (primary key - pk),
        у экзепляра класса Women берем параметр pk (self.pk)
        и динамически присваиваем его в маршрут (в параметр post_id),
        который находится в women/urls.py --> path('post/<int:post_id>/', show_post, name='post')
        Далее мы используем этот метод в шаблоне index.html для перехода по полученной динамической ссылке,
        при нажатии кнопки 'Читать пост'"""
        return reverse('post', kwargs={'post_id': self.pk})


class Category(models.Model):
    """Создаем модель (таблицу в БД) Category"""
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        """при чтении записи, вместо ссылки на объект будет возвращать имя (name) записи (Актрисы, Певицы и т.д.)"""
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})



