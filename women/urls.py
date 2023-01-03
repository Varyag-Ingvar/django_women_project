from django.urls import path
from .views import about, contact, login, WomenHome, WomenCategory, ShowPost, AddPage

urlpatterns = [
    # path('', index, name='home'),  # маршрут для функции index из модуля view (homepage)
    path('', WomenHome.as_view(), name='home'),  # маршрут для класса WomenHome из модуля view (homepage)
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),   # переделали по слагу вместо id(pk)
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
