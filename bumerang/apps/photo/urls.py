# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from bumerang.apps.utils.views import XMLDetailView, ObjectsDeleteView
from models import Photo
from albums.models import PhotoAlbum
from views import (PhotoListView, PhotoCreateView, PhotoDetailView,
    PhotoUpdateView, PhotoMoveView)
from albums.views import (PhotoAlbumCreateView, PhotoSetCoverView,
    PhotoAlbumUpdateView)


urlpatterns = patterns('',
    url(r'^album/add/$',
        login_required(PhotoAlbumCreateView.as_view()),
        name='photo-album-add'
    ),
    url(r'^album(?P<photo_album_id>[\d]+)/add/$',
        login_required(PhotoCreateView.as_view()),
        name='album-photo-add'
    ),
    url(r'^album(?P<pk>[\d]+)/$',
        DetailView.as_view(model=PhotoAlbum),
        name='photo-album-detail'
    ),
    url(r'^album(?P<pk>[\d]+)/edit/$',
        login_required(PhotoAlbumUpdateView.as_view()),
        name='photo-album-edit'
    ),
    url(r'^album(?P<pk>[\d]+)/set-cover/$',
        login_required(PhotoSetCoverView.as_view()),
        name='photo-album-cover'
    ),
    url(r'^add/$',
        login_required(PhotoCreateView.as_view()),
        name='photo-add'
    ),
    url(r'^(?P<pk>[\d]+)/edit/$',
        login_required(PhotoUpdateView.as_view()),
        name='photo-edit'
    ),
    url(r'^$',
        PhotoListView.as_view(),
        name='photo-list'
    ),
    url(r'^photos-delete/$',
        login_required(ObjectsDeleteView.as_view(model=Photo)),
        name='photos-delete'
    ),
    url(r'^albums-delete/$',
        login_required(ObjectsDeleteView.as_view(model=PhotoAlbum)),
        name='photoalbums-delete'
    ),
    url(r'^photo-move/$',
        login_required(PhotoMoveView.as_view()),
        name='photo-move'
    ),
#    url(r'^delete/(?P<pk>\w+)/$',
#        login_required(PhotoDeleteView.as_view()),
#        name='photo-delete'
#    ),
    url(r'^(?P<pk>\w+)/$',
        PhotoDetailView.as_view(),
        name='photo-detail'
    ),
)
