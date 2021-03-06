# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contest_set', null=True, to=orm['events.Event'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owned_events', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_winners', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('min_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('opened', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('requesting_till', self.gf('django.db.models.fields.DateField')()),
            ('hold_place', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('participant_conditions', self.gf('django.db.models.fields.TextField')()),
            ('contacts_raw_text', self.gf('django.db.models.fields.TextField')()),
            ('rules_document', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding model 'Juror'
        db.create_table('events_juror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('info_second_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('info_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('info_middle_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('min_avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal('events', ['Juror'])

        # Adding model 'GeneralRule'
        db.create_table('events_generalrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('events', ['GeneralRule'])

        # Adding model 'NewsPost'
        db.create_table('events_newspost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('creation_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('events', ['NewsPost'])

        # Adding model 'Nomination'
        db.create_table('events_nomination', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('age_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('age_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('events', ['Nomination'])

        # Adding model 'Participant'
        db.create_table('events_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('index_number', self.gf('django.db.models.fields.IntegerField')()),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('events', ['Participant'])

        # Adding unique constraint on 'Participant', fields ['owner', 'event']
        db.create_unique('events_participant', ['owner_id', 'event_id'])

        # Adding unique constraint on 'Participant', fields ['event', 'index_number']
        db.create_unique('events_participant', ['event_id', 'index_number'])

        # Adding model 'ParticipantVideo'
        db.create_table('events_participantvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Participant'])),
            ('nomination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_selected_participantvideo_set', to=orm['events.Nomination'])),
            ('age', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'], on_delete=models.PROTECT)),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('events', ['ParticipantVideo'])

        # Adding unique constraint on 'ParticipantVideo', fields ['participant', 'video']
        db.create_unique('events_participantvideo', ['participant_id', 'video_id'])

        # Adding model 'VideoNomination'
        db.create_table('events_videonomination', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant_video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.ParticipantVideo'])),
            ('nomination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Nomination'])),
            ('result', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('events', ['VideoNomination'])

        # Adding model 'ParticipantVideoScore'
        db.create_table('events_participantvideoscore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('participant_video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.ParticipantVideo'])),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('events', ['ParticipantVideoScore'])

    def backwards(self, orm):
        # Removing unique constraint on 'ParticipantVideo', fields ['participant', 'video']
        db.delete_unique('events_participantvideo', ['participant_id', 'video_id'])

        # Removing unique constraint on 'Participant', fields ['event', 'index_number']
        db.delete_unique('events_participant', ['event_id', 'index_number'])

        # Removing unique constraint on 'Participant', fields ['owner', 'event']
        db.delete_unique('events_participant', ['owner_id', 'event_id'])

        # Deleting model 'Event'
        db.delete_table('events_event')

        # Deleting model 'Juror'
        db.delete_table('events_juror')

        # Deleting model 'GeneralRule'
        db.delete_table('events_generalrule')

        # Deleting model 'NewsPost'
        db.delete_table('events_newspost')

        # Deleting model 'Nomination'
        db.delete_table('events_nomination')

        # Deleting model 'Participant'
        db.delete_table('events_participant')

        # Deleting model 'ParticipantVideo'
        db.delete_table('events_participantvideo')

        # Deleting model 'VideoNomination'
        db.delete_table('events_videonomination')

        # Deleting model 'ParticipantVideoScore'
        db.delete_table('events_participantvideoscore')

    models = {
        'albums.videoalbum': {
            'Meta': {'object_name': 'VideoAlbum'},
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.event': {
            'Meta': {'ordering': "('start_date', 'end_date')", 'object_name': 'Event'},
            'contacts_raw_text': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'hold_place': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jurors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'juror_events'", 'symmetrical': 'False', 'through': "orm['events.Juror']", 'to': "orm['auth.User']"}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'min_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'opened': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_events'", 'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contest_set'", 'null': 'True', 'to': "orm['events.Event']"}),
            'participant_conditions': ('django.db.models.fields.TextField', [], {}),
            'publish_winners': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requesting_till': ('django.db.models.fields.DateField', [], {}),
            'rules_document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'events.generalrule': {
            'Meta': {'object_name': 'GeneralRule'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'events.juror': {
            'Meta': {'object_name': 'Juror'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'info_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'info_second_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'min_avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'events.newspost': {
            'Meta': {'ordering': "('creation_date',)", 'object_name': 'NewsPost'},
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'events.nomination': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'Nomination'},
            'age_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'events.participant': {
            'Meta': {'unique_together': "(('owner', 'event'), ('event', 'index_number'))", 'object_name': 'Participant'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_number': ('django.db.models.fields.IntegerField', [], {}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['video.Video']", 'through': "orm['events.ParticipantVideo']", 'symmetrical': 'False'})
        },
        'events.participantvideo': {
            'Meta': {'unique_together': "(('participant', 'video'),)", 'object_name': 'ParticipantVideo'},
            'age': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'nomination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_selected_participantvideo_set'", 'to': "orm['events.Nomination']"}),
            'nominations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['events.Nomination']", 'through': "orm['events.VideoNomination']", 'symmetrical': 'False'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Participant']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']", 'on_delete': 'models.PROTECT'})
        },
        'events.participantvideoscore': {
            'Meta': {'object_name': 'ParticipantVideoScore'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'participant_video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.ParticipantVideo']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'events.videonomination': {
            'Meta': {'object_name': 'VideoNomination'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomination': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Nomination']"}),
            'participant_video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.ParticipantVideo']"}),
            'result': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'video.video': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Video'},
            'access': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'album': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '255', 'to': "orm['albums.VideoAlbum']", 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.VideoCategory']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'festivals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.VideoGenre']", 'null': 'True', 'blank': 'True'}),
            'hq_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_in_broadcast_lists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'original_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'published_in_archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teachers': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'views_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2011', 'null': 'True', 'blank': 'True'})
        },
        'video.videocategory': {
            'Meta': {'ordering': "('sort_order', 'title')", 'object_name': 'VideoCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'video.videogenre': {
            'Meta': {'ordering': "('sort_order', 'title')", 'object_name': 'VideoGenre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['events']