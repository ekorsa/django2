from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category, Post


class PostAdmin(TranslationAdmin):
    model = Post
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'post_type', 'rating', 'creation_date')
    list_filter = ('title', 'post_type', 'rating', 'creation_date')
    search_fields = ('title', 'post_category__name')


class CategoryAdmin(TranslationAdmin):
    model = Category

# class PostAdmin(TranslationAdmin):
#     model = Post

# admin.site.register(Post)
# admin.site.register(Category)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
