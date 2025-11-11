from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Article, ArticleImage, Category
from .forms import ArticleImageForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')  # показуємо назву та slug
    prepopulated_fields = {'slug': ('category',)}  # автозаповнення slug
    fieldsets = (
        ('Основне', {
            'fields': ('category', 'slug'),
        }),
    )

admin.site.register(Category, CategoryAdmin)

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    form = ArticleImageForm
    extra = 0
    fieldsets = (
        ('Зображення', {
            'fields': ('title', 'image'),
        }),
    )

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'slug', 'main_page', 'category')
    inlines = [ArticleImageInline]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category',)
    fieldsets = (
        ('Основне', {
            'fields': ('pub_date', 'title', 'description', 'main_page', 'category'),
        }),
        ('Додатково', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug',),
        }),
    )

    def delete_file(self, pk, request):
        obj = get_object_or_404(ArticleImage, pk=pk)
        obj.delete()

admin.site.register(Article, ArticleAdmin)
