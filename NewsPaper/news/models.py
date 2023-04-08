from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

# Create your models here.


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(pr=Sum('rating'))
        comment_rating = self.author_name.comment_set.aggregate(cr=Sum('rating'))
        self.rating = post_rating.get('pr') * 3 + comment_rating.get('cr')
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscription')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    news = 'N'
    article = 'A'
    ARTICLE_TYPE = [
        (news, 'News'),
        (article, 'Article'),
    ]
    title = models.CharField(max_length=256, unique=True)
    text = models.TextField()
    post_type = models.CharField(max_length=1, choices=ARTICLE_TYPE, default=news)
    rating = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    # modify_date = models.DateTimeField(auto_now=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
