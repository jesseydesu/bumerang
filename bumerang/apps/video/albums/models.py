# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from bumerang.apps.utils.models import TitleUnicode, nullable
from bumerang.apps.utils.storages import RewritableFilesStorage
from bumerang.apps.video.models import Video

def video_album_preview_upload_to(instance, filename):
    return 'previews/video-album/{0}/{1}'.format(instance.owner.slug, filename)


class VideoAlbum(models.Model, TitleUnicode):
    owner = models.ForeignKey(User)
    title = models.CharField(u'Название', max_length=100)
    description = models.TextField(u'Описание', **nullable)
    preview = models.ImageField(u'Обложка',
        upload_to=video_album_preview_upload_to, storage=RewritableFilesStorage)
    cover = models.OneToOneField(Video, on_delete=models.SET_NULL, **nullable)

    class Meta:
        verbose_name = u'Видеоальбом'
        verbose_name_plural = u'Видеоальбомы'

    def preview(self):
        if self.cover:
            return self.cover.preview()
        return None
