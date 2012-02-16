# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.deletion import ProtectedError

from bumerang.apps.utils.functions import random_string
from bumerang.apps.utils.models import TitleUnicode, nullable, choices


class PhotoCategory(models.Model, TitleUnicode):
    title = models.CharField(max_length=255, verbose_name=u"Имя")
    slug = models.SlugField()

    class Meta:
        verbose_name = u'Категория фото'
        verbose_name_plural = u'Категории фото'


class PhotoGenre(models.Model, TitleUnicode):
    title = models.CharField(max_length=255, verbose_name=u"Имя")
    slug = models.SlugField()

    class Meta:
        verbose_name = u'Жанр фото'
        verbose_name_plural = u'Жанры фото'


def original_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    return 'photos/{0}.{1}'.format(instance.slug, ext)


class Photo(models.Model, TitleUnicode):
    SLUG_LENGTH = 20

    FREE_FOR_ALL = 1
    ACCESS_URL = 2
    ACCESS_PASSWORD = 3
    ACCESS_FRIENDS = 4
    FOR_ME_ONLY = 5
    ACCESS_FLAGS_CHOICES = (
        (FREE_FOR_ALL, u'Всем пользователям'),
        (ACCESS_URL, u'Пользователем, у которых есть ссылка'),
        (ACCESS_PASSWORD, u'Пользователем, у которых есть ссылка и пароль'),
        (ACCESS_FRIENDS, u'Друзьям'),
        (FOR_ME_ONLY, u'Только мне'),
    )

    CONVERTING = 1
    READY = 2
    ERROR = 3
    STATUS_CHOICES = choices(
        (CONVERTING, u'конвертируется'),
        (READY, u'обработано'),
        (ERROR, u'ошибка обработки')
    )

    slug = models.SlugField(u'Метка', max_length=SLUG_LENGTH, editable=False)
    published_in_archive = models.BooleanField(u'Опубликовано в видеорхиве',
        default=False)
    is_in_broadcast_lists = models.BooleanField(u'Списки вещания',
        default=False)
    title = models.CharField(u'Название', max_length=255)
    slug = models.SlugField(u'Метка (часть ссылки)', **nullable)
    original_file = models.ImageField(u"Оригинальное фото",
        upload_to=original_upload_to, **nullable)
    owner = models.ForeignKey(User, verbose_name=u"Владелец")
    album = models.ForeignKey('albums.PhotoAlbum', verbose_name=u'Альбом',
        max_length=255, **nullable)
    category = models.ForeignKey(PhotoCategory, verbose_name=u'Категория',
        **nullable)
    description = models.TextField(u'Описание', **nullable)
    year = models.IntegerField(u'Год', default=2011, **nullable)
    genre = models.ForeignKey(PhotoGenre, verbose_name=u'Жанр', **nullable)
    country = models.CharField(u'Страна', max_length=255, **nullable)
    city = models.CharField(u'Город', max_length=255, **nullable)
    authors = models.CharField(u'Авторы', max_length=255, **nullable)
    agency = models.CharField(u'учреждение', max_length=255, **nullable)
    teachers = models.CharField(u'Педагоги', max_length=255, **nullable)
    manager = models.CharField(u'Руководитель', max_length=255, **nullable)
    festivals = models.TextField(u'Фестивали', **nullable)
    access = models.IntegerField(u'Кому доступно видео',
        choices=ACCESS_FLAGS_CHOICES, default=1, **nullable)
    created = models.DateTimeField(u'Дата добавления', default=datetime.now)
    views_count = models.IntegerField(u'Количество просмотров видео', default=0,
                                      editable=False, **nullable)
    status = models.IntegerField(u'статус', choices=STATUS_CHOICES)

    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'
        ordering = ('-id',)

    def __init__(self, *args, **kwargs):
        super(Photo, self).__init__(*args, **kwargs)
        if not self.slug:
            self.slug = self.get_slug()

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        if self.album:
            if not self.album.cover:
                self.album.cover = self
                self.album.save()

    def delete(self, **kwargs):
        paths = []
        for field in self._meta.fields:
            if issubclass(field.__class__, models.FileField):
                file_field = getattr(self, field.name)
                if 'path' in file_field:
                    if os.path.isfile(file_field.path):
                        paths.append(file_field.path)
        try:
            super(Photo, self).delete(**kwargs)
            for path in paths:
                try:
                    os.remove(path)
                except OSError:
                    print 'failed remove the file'
        except ProtectedError:
            pass #TODO: raise delete error, say it to user

    def get_absolute_url(self):
        return reverse('video-detail', kwargs={'pk': self.pk})

    @classmethod
    def get_slug(cls):
        while True:
            slug = random_string(cls.SLUG_LENGTH)
            if not cls.objects.filter(slug=slug).exists():
                return slug
