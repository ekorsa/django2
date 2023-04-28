from django.contrib import admin

from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'post_type', 'rating', 'creation_date')
    list_filter = ('title', 'post_type', 'rating', 'creation_date')
    search_fields = ('title', 'post_category__name')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
