# Generated by Django 4.0.6 on 2022-09-01 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_blog_blog_date_bc9b9d_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tag_text',
            field=models.TextField(default=''),
        ),
    ]