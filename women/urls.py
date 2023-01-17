from django.urls import path
from django.views.decorators.cache import cache_page
"""cache_page - декоратор для кэширования страниц сайта, 
при использовании функций-представлений декорируются сами функции в views.py, если используем классы - то прописываем 
в маршрутах, также необходимо прописать пути к папке кэша в настройках. 
Ниже закешируем homepage"""

from .views import about, WomenHome, WomenCategory, ShowPost, AddPage, RegisterUser, LoginUser, logout_user, \
    ContactFormView

urlpatterns = [
    # path('', index, name='home'),  # маршрут для функции index из модуля view (homepage)
    path('', cache_page(60)(WomenHome.as_view()), name='home'),  # маршрут для класса WomenHome из модуля view (homepage)
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),   # переделали по слагу вместо id(pk)
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
