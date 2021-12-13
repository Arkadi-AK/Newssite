from django.db import models
from django.urls import reverse


# Create your models here.


class News(models.Model):  # Модель(таблица) новостей вторичная
    title = models.CharField(max_length=150, verbose_name='Наименование новости')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото',
                              blank=True)  # Чтобы новость можно было добавлять без фото (сделать необязательным поле 'Фото' blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 verbose_name='Категория новости')  # Категория новости (ссылку на модель (Category) делать если первичная модель объявлена раньше), так как она нах ниже, то указываем строкой). models.PROTECT -защита от удаления. "null=True" - позволит не заполнять это поле
    views = models.IntegerField(default=0)


    def get_absolute_url(self):  # По конвенции Джанго этот метод принято называть "get_absolute_url". Этот  метод будет указывать на конкретную категорию и строить нужный вариант ссылки. Испоользу такое имя Джанго сам должен выстроить ссылку. В админке добавится кнопка "Смотреть на сайте"
        return reverse('view_news', kwargs={'pk': self.pk}) # news_id используется при работе с функцией. При работе с классом ViewNews использовать 'pk'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'  # Название новости в единственном числе в админке
        verbose_name_plural = 'Новости'  # Название новости во множественном числе в админке
        ordering = ['created_at']  # Сортировка новостей по дате создания


class Category(models.Model):  # Создание модели категорий новостей (Модель Category будет первичной)
    title = models.CharField(max_length=150, db_index=True,
                             verbose_name='Наименование категории')  # db_index=True Индексирует поле индекс, делает его быстрым для поиска

    def get_absolute_url(self):  # По конвенции Джанго этот метод принято называть "get_absolute_url". Этот  метод будет указывать на конкретную категорию и строить нужный вариант ссылки. Испоользу такое имя Джанго сам должен выстроить ссылку. В админке добавится кнопка "Смотреть на сайте"
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'  # Название категории новости в единственном числе в админке
        verbose_name_plural = 'Категории'  # Название категории во множественном числе в админке
        ordering = ['title']  # Сортировка категорий по дате создания
