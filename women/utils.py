from women.models import Category

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


class DataMixin:
    """Создается для того чтобы убрать дублирование кода из классов представлений в women/views.py"""

    paginate_by = 1  # количество постов отображаемых на странице (вынесено в DataMixin)

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:   # если мы не передавали в context 'cat_selected'
            context['cat_selected'] = 0     # то делаем его по умолчанию равным нулю
        return context

