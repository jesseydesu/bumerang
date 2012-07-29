# -*- coding: utf-8 -*-
"""
make sure you have this setting
AWS_PRELOAD_METADATA = True
and that you have python-dateutils==1.5 installed
"""
from __future__ import absolute_import

from django.conf import settings

from boto.utils import parse_ts
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

    def modified_time(self, name):
        name = self._normalize_name(self._clean_name(name))
        entry = self.entries.get(name)
        if entry is None:
            entry = self.bucket.get_key(self._encode_name(name))
            # Parse the last_modified string to a local datetime object.
        return parse_ts(entry.last_modified)


if settings.LOCALHOST:
    from storages.backends.overwrite import OverwriteStorage
    media_storage = OverwriteStorage()
else:
    media_storage = CachedS3BotoStorage(
        bucket=settings.AWS_MEDIA_STORAGE_BUCKET_NAME,
        custom_domain=settings.AWS_S3_MEDIA_CUSTOM_DOMAIN
    )
