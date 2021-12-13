from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),


    path('test/', test, name='test'),
    # path('', index, name='home'), # Этот маршрут работает для ФУНКЦИЙ из views.py. Либо этот, либо с классами
    path('', HomeNews.as_view(), name='home'),  # Этот маршрут для работы КЛАССОВ из views.py.
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),  # Этот маршрут для работы КЛАССОВ из views.py. Так же (можно) ЗАКЭШИРУЕМ всю страницу "ГЛАВНАЯ" на 60 сек

    # path('category/<int:category_id>/', get_category, name='category'), # Это для работы с функцией
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),  # Это для работы с классом

    # path('news/<int:news_id>/', view_news, name='view_news'), # Этот маршрут для работы функции view_news
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),

    # path('news/add_news/', add_news, name='add_news'), # этот маршрут при работе с функцией add_news
    path('news/add_news/', CreateNews.as_view(), name='add_news'), # этот при работе с классом


]
