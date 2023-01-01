from django.urls import path
from .views import about, addpage, contact, login, show_post, show_category, WomenHome

urlpatterns = [
    # path('', index, name='home'),  # маршрут для функции index из модуля view (homepage)
    path('', WomenHome.as_view(), name='home'),  # маршрут для класса WomenHome из модуля view (homepage)
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),   # переделали по слагу вместо id(pk)
    path('category/<slug:cat_slug>/', show_category, name='category'),
]
