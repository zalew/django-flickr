# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FlickrUser'
        db.create_table('flickr_flickruser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('flickr_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('nsid', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('realname', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('photosurl', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('profileurl', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('mobileurl', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('iconserver', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('iconfarm', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('path_alias', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('perms', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('flickr', ['FlickrUser'])

        # Adding model 'Photo'
        db.create_table('flickr_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flickr_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flickr.FlickrUser'])),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('server', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('farm', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('originalsecret', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_taken_granularity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('url_page', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, null=True, blank=True)),
            ('square_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('square_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('square_source', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('square_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('thumb_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('thumb_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('thumb_source', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('thumb_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('small_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('small_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('small_source', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('small_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('medium_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('medium_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('medium_source', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('medium_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('large_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('large_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('large_source', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('large_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('ori_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ori_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ori_source', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('ori_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('exif', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exif_camera', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('exif_exposure', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('exif_aperture', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('exif_iso', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exif_focal', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('exif_flash', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('ispublic', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('isfriend', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('isfamily', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('geo_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_accuracy', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(default=0, max_length=50)),
        ))
        db.send_create_signal('flickr', ['Photo'])

        # Adding model 'PhotoSet'
        db.create_table('flickr_photoset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flickr_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flickr.FlickrUser'])),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('server', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('farm', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('primary', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('flickr', ['PhotoSet'])

        # Adding M2M table for field photos on 'PhotoSet'
        db.create_table('flickr_photoset_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photoset', models.ForeignKey(orm['flickr.photoset'], null=False)),
            ('photo', models.ForeignKey(orm['flickr.photo'], null=False))
        ))
        db.create_unique('flickr_photoset_photos', ['photoset_id', 'photo_id'])

        # Adding model 'JsonCache'
        db.create_table('flickr_jsoncache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flickr_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sizes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exif', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exception', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('flickr', ['JsonCache'])


    def backwards(self, orm):
        
        # Deleting model 'FlickrUser'
        db.delete_table('flickr_flickruser')

        # Deleting model 'Photo'
        db.delete_table('flickr_photo')

        # Deleting model 'PhotoSet'
        db.delete_table('flickr_photoset')

        # Removing M2M table for field photos on 'PhotoSet'
        db.delete_table('flickr_photoset_photos')

        # Deleting model 'JsonCache'
        db.delete_table('flickr_jsoncache')


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
        'flickr.flickruser': {
            'Meta': {'ordering': "['id']", 'object_name': 'FlickrUser'},
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'iconfarm': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iconserver': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'large_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'large_source': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'large_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'large_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '50'}),
            'medium_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'medium_source': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'medium_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'medium_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ori_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ori_source': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ori_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ori_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'originalsecret': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'server': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'small_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'small_source': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'small_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'small_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'square_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'square_source': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'square_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'square_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_source': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumb_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_page': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flickr.FlickrUser']"})
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
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
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
