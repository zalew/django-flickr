# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhotoSizeData'
        db.create_table('flickr_photosizedata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sizes', to=orm['flickr.Photo'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('flickr', ['PhotoSizeData'])

        # Adding unique constraint on 'PhotoSizeData', fields ['photo', 'size']
        db.create_unique('flickr_photosizedata', ['photo_id', 'size'])

        # Deleting field 'Photo.thumb_source'
        db.delete_column('flickr_photo', 'thumb_source')

        # Deleting field 'Photo.medium_url'
        db.delete_column('flickr_photo', 'medium_url')

        # Deleting field 'Photo.ori_height'
        db.delete_column('flickr_photo', 'ori_height')

        # Deleting field 'Photo.large_url'
        db.delete_column('flickr_photo', 'large_url')

        # Deleting field 'Photo.square_source'
        db.delete_column('flickr_photo', 'square_source')

        # Deleting field 'Photo.square_height'
        db.delete_column('flickr_photo', 'square_height')

        # Deleting field 'Photo.square_url'
        db.delete_column('flickr_photo', 'square_url')

        # Deleting field 'Photo.medium_width'
        db.delete_column('flickr_photo', 'medium_width')

        # Deleting field 'Photo.large_source'
        db.delete_column('flickr_photo', 'large_source')

        # Deleting field 'Photo.large_width'
        db.delete_column('flickr_photo', 'large_width')

        # Deleting field 'Photo.large_height'
        db.delete_column('flickr_photo', 'large_height')

        # Deleting field 'Photo.small_source'
        db.delete_column('flickr_photo', 'small_source')

        # Deleting field 'Photo.square_width'
        db.delete_column('flickr_photo', 'square_width')

        # Deleting field 'Photo.thumb_width'
        db.delete_column('flickr_photo', 'thumb_width')

        # Deleting field 'Photo.small_width'
        db.delete_column('flickr_photo', 'small_width')

        # Deleting field 'Photo.thumb_height'
        db.delete_column('flickr_photo', 'thumb_height')

        # Deleting field 'Photo.ori_url'
        db.delete_column('flickr_photo', 'ori_url')

        # Deleting field 'Photo.small_url'
        db.delete_column('flickr_photo', 'small_url')

        # Deleting field 'Photo.thumb_url'
        db.delete_column('flickr_photo', 'thumb_url')

        # Deleting field 'Photo.ori_width'
        db.delete_column('flickr_photo', 'ori_width')

        # Deleting field 'Photo.medium_source'
        db.delete_column('flickr_photo', 'medium_source')

        # Deleting field 'Photo.small_height'
        db.delete_column('flickr_photo', 'small_height')

        # Deleting field 'Photo.medium_height'
        db.delete_column('flickr_photo', 'medium_height')

        # Deleting field 'Photo.ori_source'
        db.delete_column('flickr_photo', 'ori_source')


        # Changing field 'Photo.originalsecret'
        db.alter_column('flickr_photo', 'originalsecret', self.gf('django.db.models.fields.CharField')(default='', max_length=10))

        # Changing field 'PhotoDownload.image_file'
        db.alter_column('flickr_photodownload', 'image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

        # Changing field 'FlickrUser.last_sync'
        db.alter_column('flickr_flickruser', 'last_sync', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'PhotoSizeData', fields ['photo', 'size']
        db.delete_unique('flickr_photosizedata', ['photo_id', 'size'])

        # Deleting model 'PhotoSizeData'
        db.delete_table('flickr_photosizedata')

        # Adding field 'Photo.thumb_source'
        db.add_column('flickr_photo', 'thumb_source',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.medium_url'
        db.add_column('flickr_photo', 'medium_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.ori_height'
        db.add_column('flickr_photo', 'ori_height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.large_url'
        db.add_column('flickr_photo', 'large_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.square_source'
        db.add_column('flickr_photo', 'square_source',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.square_height'
        db.add_column('flickr_photo', 'square_height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.square_url'
        db.add_column('flickr_photo', 'square_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.medium_width'
        db.add_column('flickr_photo', 'medium_width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.large_source'
        db.add_column('flickr_photo', 'large_source',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.large_width'
        db.add_column('flickr_photo', 'large_width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.large_height'
        db.add_column('flickr_photo', 'large_height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.small_source'
        db.add_column('flickr_photo', 'small_source',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.square_width'
        db.add_column('flickr_photo', 'square_width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.thumb_width'
        db.add_column('flickr_photo', 'thumb_width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.small_width'
        db.add_column('flickr_photo', 'small_width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.thumb_height'
        db.add_column('flickr_photo', 'thumb_height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.ori_url'
        db.add_column('flickr_photo', 'ori_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.small_url'
        db.add_column('flickr_photo', 'small_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.thumb_url'
        db.add_column('flickr_photo', 'thumb_url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.ori_width'
        db.add_column('flickr_photo', 'ori_width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.medium_source'
        db.add_column('flickr_photo', 'medium_source',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.small_height'
        db.add_column('flickr_photo', 'small_height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.medium_height'
        db.add_column('flickr_photo', 'medium_height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.ori_source'
        db.add_column('flickr_photo', 'ori_source',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Photo.originalsecret'
        db.alter_column('flickr_photo', 'originalsecret', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'PhotoDownload.image_file'
        db.alter_column('flickr_photodownload', 'image_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'FlickrUser.last_sync'
        db.alter_column('flickr_flickruser', 'last_sync', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=None))

    models = {
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
        'flickr.collection': {
            'Meta': {'ordering': "('-date_created',)", 'object_name': 'Collection'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flickr.Collection']", 'null': 'True'}),
            'sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['flickr.PhotoSet']", 'null': 'True', 'symmetrical': 'False'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flickr.FlickrUser']"})
        },
        'flickr.flickruser': {
            'Meta': {'ordering': "['id']", 'object_name': 'FlickrUser'},
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'iconfarm': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iconserver': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mobileurl': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nsid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'path_alias': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'perms': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'photosurl': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profileurl': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'flickr.jsoncache': {
            'Meta': {'object_name': 'JsonCache'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'exception': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exif': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sizes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'flickr.photo': {
            'Meta': {'ordering': "('-date_posted', '-date_taken')", 'object_name': 'Photo'},
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_taken_granularity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exif': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exif_aperture': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'exif_camera': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'exif_exposure': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'exif_flash': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'exif_focal': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'exif_iso': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'farm': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'geo_accuracy': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isfamily': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'isfriend': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ispublic': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '50'}),
            'originalformat': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'originalsecret': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'server': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_page': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flickr.FlickrUser']"})
        },
        'flickr.photodownload': {
            'Meta': {'object_name': 'PhotoDownload'},
            'date_downloaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ori': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flickr.Photo']", 'unique': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'flickr.photoset': {
            'Meta': {'ordering': "('-date_posted', '-id')", 'object_name': 'PhotoSet'},
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'farm': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['flickr.Photo']", 'null': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'server': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flickr.FlickrUser']"})
        },
        'flickr.photosizedata': {
            'Meta': {'unique_together': "(('photo', 'size'),)", 'object_name': 'PhotoSizeData'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sizes'", 'to': "orm['flickr.Photo']"}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['flickr']