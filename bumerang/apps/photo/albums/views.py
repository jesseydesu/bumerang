# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin

from bumerang.apps.utils.views import OwnerMixin
from forms import PhotoAlbumForm, PhotoAlbumCoverForm
from models import PhotoAlbum


class PhotoSetCoverView(UpdateView):
    model = PhotoAlbum
    form_class = PhotoAlbumCoverForm

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, u'Обложка фотоальбома обновлена')
        return reverse('photo-album-detail', args=[self.object.id])


class PhotoAlbumUpdateView(OwnerMixin, UpdateView):
    model = PhotoAlbum
    form_class = PhotoAlbumForm

    def get_success_url(self):
        return reverse('photo-album-detail', kwargs={'pk': self.object.id})


class PhotoAlbumCreateView(CreateView):
    model = PhotoAlbum
    form_class = PhotoAlbumForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('album-photo-add',
            kwargs={'photo_album_id': self.object.id})
