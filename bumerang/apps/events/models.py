# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
import os

from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from bumerang.apps.utils.media_storage import media_storage
from bumerang.apps.utils.models import TitleUnicode, FileModelMixin
from bumerang.apps.video.models import Video


nullable = dict(null=True, blank=True)

def get_juror_avatar_path(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'jurors', str(instance.id))
    if not os.path.exists(path):
        os.makedirs(path)
    ext = os.path.splitext(filename)[1]
    return 'jurors_avatars/{0}/min{1}'.format(instance.id, ext)

def get_event_rules_path(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'event_rules', str(instance.id))
    if not os.path.exists(path):
        os.makedirs(path)
    return 'event_rules/{0}/{1}'.format(instance.id, filename)

def get_logo_path(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'logos', str(instance.id))
    if not os.path.exists(path):
        os.makedirs(path)
    ext = os.path.splitext(filename)[1]
    return u'logos/{0}/full{1}'.format(instance.id, ext)

def get_mini_logo_path(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'logos', str(instance.id))
    if not os.path.exists(path):
        os.makedirs(path)
    ext = os.path.splitext(filename)[1]
    return u'logos/{0}/min{1}'.format(instance.id, ext)


class Event(FileModelMixin, models.Model):
    CONTEST = 1
    FESTIVAL = 2
    TYPES_CHOICES = (
        (CONTEST, u'Конкурс'),
        (FESTIVAL, u'Фестиваль'),
    )
    parent = models.ForeignKey('self', verbose_name=u'В рамках фестиваля',
        related_name='contest_set', **nullable)
    owner = models.ForeignKey(User, related_name='owned_events')
    type = models.IntegerField(u'Тип события', choices=TYPES_CHOICES)
    is_approved = models.BooleanField(u'Заявка подтверждена', default=False)

    logo = models.ImageField(u'Логотип фестиваля',
        upload_to=get_logo_path, storage=media_storage, **nullable)
    min_logo = models.ImageField(u'Уменьшенный логотип фестиваля',
        upload_to=get_mini_logo_path, storage=media_storage, **nullable)

    title = models.CharField(u'Название события', max_length=255)
    opened = models.BooleanField(u'Фестиваль открыт', default=True)
    start_date = models.DateField(u'Дата начала')
    end_date = models.DateField(u'Дата окончания')
    requesting_till = models.DateField(u'Прием заявок до')
    hold_place = models.TextField(u'Место проведения')
    description = models.TextField(u'Описание фестиваля')
#    text_rules = models.TextField(u'Правила фестиваля', blank=False)
#    file_rules = models.FileField(u'Правила фестиваля ( документ )',
#        upload_to='events_rules', storage=media_storage, blank=True)
    participant_conditions = models.TextField(u'Условия подачи заявок',
        blank=False)
    contacts_raw_text = models.TextField(u'Контакты', **nullable)

    created = models.DateTimeField(u'Дата добавления', default=now,
        editable=False)

    jurors = models.ManyToManyField(User, verbose_name=u'Члены жюри',
        through='Juror', related_name='juror_events')

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
        ordering = ('start_date', 'end_date')

    def __unicode__(self):
        title = self.title
        if self.type == self.FESTIVAL:
            year_string = str(self.start_date.year)
            if self.start_date.year != self.end_date.year:
                year_string += '&mdash;{0}'.format(self.end_date.year)
            title += ' {0}'.format(year_string)
        return mark_safe(title)

    def chain(self):
        return Event.objects.filter(title=self.title, owner=self.owner,
            is_approved=True, type=self.FESTIVAL)

    def contests(self):
        return self.contest_set.filter(is_approved=True)

    def is_accepting_requests(self):
        if self.requesting_till > now().date():
            return True
        return False


class Juror(FileModelMixin, models.Model):
    event = models.ForeignKey(Event, verbose_name=u'Событие')
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    email = models.EmailField(_('e-mail address'))
    info_second_name = models.CharField(u'Фамилия', max_length=100)
    info_name = models.CharField(u'Имя', max_length=100)
    info_middle_name = models.CharField(u'Отчество', max_length=100)
    #TODO: just do it
    min_avatar = models.ImageField(u'Фото',
        upload_to=get_juror_avatar_path, storage=media_storage, **nullable)

    class Meta:
        verbose_name = u'Член жюри'
        verbose_name_plural = u'Члены жюри'


class GeneralRule(TitleUnicode, models.Model):
    event = models.ForeignKey(Event, verbose_name=u'Событие')
    title = models.CharField(u'Заголовок', max_length=255)
    description = models.TextField(u'Описание')

    class Meta:
        verbose_name = u'Общие положения'
        verbose_name_plural = u'Общие положения'


class NewsPost(TitleUnicode, models.Model):
    event = models.ForeignKey(Event, verbose_name=u'Событие')
    title = models.CharField(u'Новость', max_length=255)
    description = models.TextField(u'Описание')
    creation_date = models.DateField(u'Дата добавления',
        editable=False, default=now)

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'
        ordering = ('creation_date',)


class Nomination(models.Model):
    event = models.ForeignKey(Event, verbose_name=u'Фестиваль')
    title = models.CharField(u'Название номинации', max_length=255)
    description = models.CharField(u'Описание', max_length=255, blank=True)
    age_from = models.PositiveSmallIntegerField(
        u'Возраст от (включительно)', **nullable)
    age_to = models.PositiveSmallIntegerField(u'Возраст до (включительно)',
        **nullable)
    sort_order = models.PositiveSmallIntegerField(u'Сортировка')

    class Meta:
        verbose_name = u'Номинация'
        verbose_name_plural = u'Номинации'
        ordering = ('sort_order',)

    def __unicode__(self):
        if self.age_from or self.age_to:
            age_postfix = u' ('
            if self.age_from:
                age_postfix += u'от {0} '.format(self.age_from)
            if self.age_to:
                age_postfix += u'до {0} '.format(self.age_to)
            age_postfix += u'лет)'
        else:
            age_postfix = u' (без возрастных ограничений)'
        return self.title + age_postfix


class Participant(models.Model):
    owner = models.ForeignKey(User, verbose_name=u'Участник')
    event = models.ForeignKey(Event, verbose_name=u'Фестиваль')
    index_number = models.IntegerField(u'Номер заявки', editable=False)
    is_accepted = models.BooleanField(u'Заявка принята', default=False)
    videos = models.ManyToManyField(Video,
        verbose_name=u'Видео', through='ParticipantVideo')

    class Meta:
        unique_together = (
            ('owner', 'event'),
            ('event', 'index_number')
        )

    def __unicode__(self):
        return u'{0} в {1}'.format(self.owner, self.event)

    def save(self, *args, **kwargs):
        self.index_number = (self.__class__.objects.filter(event=self.event
            ).aggregate(Max('index_number'))['index_number__max'] or 0) + 1
        super(Participant, self).save(*args, **kwargs)


class ParticipantVideo(models.Model):
    participant = models.ForeignKey(Participant,
        verbose_name=u'Заявка на фестиваль')
    nomination = models.ForeignKey(Nomination, verbose_name=u'Номинация',
        related_name='user_selected_participantvideo_set')
    nominations = models.ManyToManyField(Nomination, verbose_name=u'Номинации',
        through='VideoNomination', blank=False)
    age = models.PositiveSmallIntegerField(u'Возраст автора', blank=False)
    video = models.ForeignKey(Video, verbose_name=u'Видео', blank=False)
    is_accepted = models.BooleanField(u'Видео принято', default=False)

    class Meta:
        unique_together = (("participant", "video"),)

    def __unicode__(self):
        return u'{0}, {1} лет'.format(self.video, self.age)

    def save(self, *args, **kwargs):
        super(ParticipantVideo, self).save(*args, **kwargs)


class VideoNomination(models.Model):
    WINNER = 1
    SECOND = 2
    THIRD = 3
    STATUS_CHOICES = (
        (WINNER, u'Победитель'),
        (SECOND, u'2 место'),
        (THIRD, u'3 место'),
    )
    participant_video = models.ForeignKey(ParticipantVideo,
        verbose_name=u'Видео участника')
    nomination = models.ForeignKey(Nomination, verbose_name=u'Номинация')
    result = models.PositiveSmallIntegerField(u'Итог', choices=STATUS_CHOICES,
        **nullable)

    def __unicode__(self):
        return u'{0} в номинации {1}'.format(
            self.participant_video, self.nomination)
