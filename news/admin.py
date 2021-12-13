from django.contrib import admin
from django.utils.safestring import mark_safe

from django import forms
from .models import News, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = (
        'id', 'title', 'category', 'created_at', 'updated_at', 'is_published',
        'get_photo')  # Добавление столбцов в админке.
    list_display_links = ('id', 'title')  # Чтобы в админке название новости стало ссылкой(а не только id)
    search_fields = ('title', 'content')  # Поиск по полям в админке( указать по каким полям)
    list_editable = ('is_published',)  # Можно сделать, чтобы редактировалось поле опубликовано из админки
    list_filter = ('is_published', 'category')  # фильтровать
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at',
              'updated_at')  # Чтобы выводилась фото в админке, при создании новости.
    readonly_fields = ('get_photo', 'views', 'created_at',
                       'updated_at')  # Тут указываются поля, которые нужны только для чтения. Их пользователь не может менять
    save_on_top = True  # Добавляет панель с кнопками (сохранить..) сверху в админке

    def get_photo(self, obj):  # Для вывода картинки в админке новостей
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')  # Помечает данную строку как HTML код.
        else:
            return 'Фото не установлено'

    get_photo.short_description = "Миниатюра"  # Переименование столбца с фото в админке.....


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News,
                    NewsAdmin)  # Чтобы столбцы отобразились нужно зарегистрировать (добавить) NewsAdmin, порядок добавления важен

admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
