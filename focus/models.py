from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.

class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)

    def __str__(self):
        return self.username


class Column(models.Model):
    name = models.CharField('name', max_length=256)
    intro = models.TextField('intro', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = 'column'
        ordering = ['name']


class ArticleManager(models.Manager):
    def query_by_column(self, column_id):
        query = self.get_queryset().filter(column_id=column_id)
        return query

    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list

    def query_by_polls(self):
        query = self.get_queryset().order_by('poll_num')

    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query


class Article(models.Model):
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='belong to')
    title = models.CharField('title', max_length=256)
    author = models.ForeignKey('Author')
    user = models.ManyToManyField('NewUser', blank=True)
    content = models.TextField('content')
    pub_date = models.DateTimeField('pub_date', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('update_time', auto_now=True, null=True)
    published = models.BooleanField('notDraft', default=True)
    poll_num = models.IntegerField('poll_num', default=0)
    comment_num = models.IntegerField('comment_num', default=0)
    keep_num = models.IntegerField('keep_num', default=0)
    object = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'article'


class Comment(models.Model):
    user = models.ForeignKey('NewUser', null=True)
    article = models.ForeignKey(Article, null=True)
    content = models.TextField('content')
    pub_date = models.DateTimeField('pub_date', auto_now_add=True, editable=True)
    poll_num = models.IntegerField('poll_num', default=0)

    def __str__(self):
        return self.content


class Author(models.Model):
    name = models.CharField('name', max_length=256)
    profile = models.CharField('profile', default='', max_length=256)
    password = models.CharField('password', max_length=256)
    register_date = models.DateTimeField('register_date', auto_now_add=True, editable=True)

    def __str__(self):
        return self.name


class Poll(models.Model):
    user = models.ForeignKey('NewUser', null=True)
    article = models.ForeignKey(Article, null=True)
    comment = models.ForeignKey(Comment, null=True)
