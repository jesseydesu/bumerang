# -*- coding: utf-8 -*-
import os
import random
import subprocess

from django.conf import settings
from celery.task import Task

from models import Preview, Video
from converting.models import ConvertOptions


class MakeScreenShots(Task):
    def run(self, video, **kwargs):
        """
        Converts the Video and creates the related files.
        """
        logger = self.get_logger(**kwargs)
        logger.info("Starting Video Post conversion: %s" % video)

        Video.objects.filter(pk=video.id).update(status=video.CONVERTING)
        for preview in video.preview_set.all():
            os.remove(preview.image.path)
            preview.delete()
        options = ConvertOptions.objects.get(title='hq_file')
        size = '{0}x{1}'.format(options.width, options.height)
        source_path = video.best_quality_file().path
        duration = video.seconds_duration()
        if duration > 30:
            offset = 10
        else:
            offset = 1
        screenable_duration = duration - offset * 2
        previews_count = settings.PREVIEWS_COUNT
        if screenable_duration < 1:
            previews_count = screenable_duration = 1
        elif screenable_duration < previews_count:
            previews_count = screenable_duration
        step = screenable_duration / previews_count
        counter = 0
        while counter < previews_count:
            preview = Preview(owner=video)
            upload_to = preview.image.field.upload_to(
                preview, '{0}.jpg'.format(offset))
            output = preview.image.field.storage.path(upload_to)
            parent_path = os.path.split(output)[0]
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            cmd = self.get_commandline(source_path,
                random.choice(range(offset, offset+step)), size, output)
            process = subprocess.call(cmd, shell=False)
            if not process:
                preview.image = upload_to
                preview.save()
            offset += step
            counter += 1
        video = Video.objects.get(pk=video.id)
        video.status = Video.READY
        video.save()
        return "Ready"

    def get_commandline(self, path, offset, size, output):
        return ['ffmpeg', '-itsoffset', '-{0}'.format(offset), '-i', path,
                '-vframes', '1', '-an', '-vcodec', 'mjpeg', '-f', 'rawvideo',
                '-s', size, output]


class ConvertVideoTask(Task):

    def get_commandline(self):
        return (['HandBrakeCLI', '-O', '-C', '2', '-i', self.original_file_path]
            + self.convert_options + ['-o', self.result_file])

    def run(self, video, **kwargs):
        """
        Converts the Video and creates the related files.
        """
        #TODO: what if video will be deleted during converting?
        #what if user update videofile during converting
        logger = self.get_logger(**kwargs)
        logger.info("Starting Video Post conversion: %s" % video)

        self.original_file_path = video.original_file.path
        video.status = video.CONVERTING
        video.save()
        for options in ConvertOptions.objects.all():
            file_field_name = options.title
            field = getattr(video, file_field_name).field
            upload_to = field.upload_to(video, '')
            self.result_file = field.storage.path(upload_to)
            self.convert_options = options.as_commandline()
            setattr(video, file_field_name, None)
            video.save()
            process = subprocess.call(self.get_commandline(), shell=False)
            video = Video.objects.get(pk=video.id)
            if process:
                video.status = video.ERROR
            else:
                setattr(video, file_field_name, upload_to)
            video.save()
        MakeScreenShots.delay(video)
        return "Ready"
