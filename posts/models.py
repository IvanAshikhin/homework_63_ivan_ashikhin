from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    description = models.CharField(verbose_name='Описание', null=False, max_length=200)
    image = models.CharField(max_length=10000, null=False, verbose_name='Фото')
    author = models.ForeignKey(verbose_name='Автор', to=get_user_model(), related_name='posts', null=False, blank=False,
                               on_delete=models.CASCADE)
    likes_count = models.PositiveIntegerField(verbose_name='Количество лайков', default=0)
    comments_count = models.PositiveIntegerField(verbose_name='Количество комментариев', default=0)


class Comment(models.Model):
    author = models.ForeignKey(verbose_name='Автор', to=get_user_model(), related_name='comments', null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(verbose_name='Публикация', to='posts.Post', related_name='comments', null=False,
                             blank=False,
                             on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Комментарий', null=False, blank=False, max_length=200)
