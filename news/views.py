from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from django.core.paginator import Paginator

def test(request): # Тестовая функция для создания номеров страниц типа 1,2...22 Постраничная пагинация. Если в классе то это добавить свойство paginate_by
    objects = ['a1', 'b2', 'c3', 'd4', 'e5', 'f6', 'g7']
    paginator = Paginator(objects, 3)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test2.html', {'page_obj': page_objects})



class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # queryset = News.objects.select_related('category') # Можно и тут добавить
    mixin_prop = 'hello world'
    paginate_by = 2

    # extra_context = {'title': 'Главная'} # Этот метод использовать желательно для статичных данных. Для динамичных данных и списков использовать не рекомендуется. для этого есть get_contex_data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница') # Применение миксина
        context['mixin_prop'] = self.get_prop()
        return context


    def get_queryset(self):  # Это добавлен метод для фильтрации новостей на главной с пометкой ОПУБЛИКОВАНО
        # return News.objects.filter(is_published=True) # Это обычной запрос, создает много запросов в БД
        # Метод для меньшего числа запросов в БД. Все запросы формируются и отправляются одним заросом
        # Используется когда связь с моделями ForeignKey
        # Если метод Many-to-Many то подойдет метод priefetch
        return News.objects.filter(is_published=True).select_related('category')



# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',}
#     return render(request, template_name='news/index.html', context=context)


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):  # Это добавлен метод для фильтрации новостей на главной с пометкой ОПУБЛИКОВАНО
        # return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True) # Это обычный метод. Создается много запросов в БД
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category') # Метод для меньшего числа запросов в БД


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News  # Указываем с какой моделью будем работать. т.е будем получать данные из таблицы новостей
    # pk_url_kwarg = "news_id" # сюда приходит параметр из urls. Но можно переименовать строку в файле urls <int:news_id> в news/<int:pk>/
    # template_name = 'news/news_detail.html' # По умолчанию используется шаблон news_detail.html, но можно указать другой
    context_object_name = 'news_item'

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')  # Указывается путь для редиректа, если не указывать будет отрабатывать функция get_absolute_url из модели.
    # Функцию reverse Django сюда не принимает.
    # Если не делать success_url, то джанго будет использовать get_absolute_url, который сделает редирект на созданный объект
    # login_url = '/admin/' # Если пользователь неавторизован и хочет добавить новость, то перекинет на стр авторизации. Либо использовать raise_exception
    raise_exception = True # Либо если неавторизован выкинет ошибку 403


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)  # поле category_id из ДБ(поле category создается в ДБ уже с id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})


# def view_news(request, news_id): # Вместо этой функции может работать класс ViewNews
#     # news_item = News.objects.get(pk=news_id) # Так тоже работает
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})  # Теперь вместо ошибки 500 выдать 404


# def add_news(request): # Функция добавления новости в БД
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news_now = News.objects.create(**form.cleaned_data) # Этод метод нужен для несвязных форм с моделями
#             news_now = form.save()  # Это дл связных форм с моделями
#             return redirect(news_now)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


######################################################################
# Создание регистрации пользователей. Обычно нужно создавать отдельное приложение (как news)
# для регистрации

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # так не происходит вход при регистрауии
            # Можно сразу при регистрации, залогинить пользователя, чтобы он уже зашел в систему после регистрации
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request): # Тестовая функция для отправки писем со страницы
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'почта исх@yandex.ru', ['почта ВХод@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {"form": form})