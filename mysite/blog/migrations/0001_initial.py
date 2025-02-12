# Generated by Django 4.0.6 on 2022-08-30 03:20

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.TextField()),
                ('pub_date', models.CharField(max_length=200)),
                ('date', models.BigIntegerField(default=0)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('author_name', models.CharField(max_length=100)),
                ('author_popularity', models.CharField(max_length=100)),
                ('author_fans', models.CharField(max_length=100)),
                ('like', models.CharField(max_length=100)),
                ('collect', models.CharField(max_length=100)),
                ('read', models.CharField(max_length=100)),
                ('hot', models.BigIntegerField(default=0)),
                ('url', models.CharField(max_length=100)),
                ('show_text', models.CharField(max_length=100)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('public_date', models.DateTimeField(verbose_name='date published')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
            ],
        ),
    ]
