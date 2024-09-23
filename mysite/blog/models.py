from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.
class Blog(models.Model):
    article = models.TextField()
    pub_date = models.CharField(max_length=200)
    date = models.BigIntegerField(default=0)
    title = models.CharField(max_length=200)
    text = models.TextField()
    author_name = models.CharField(max_length=100)
    author_popularity = models.CharField(max_length=100)
    author_fans = models.CharField(max_length=100)
    like = models.CharField(max_length=100)
    collect = models.CharField(max_length=100)
    read = models.CharField(max_length=100)
    hot = models.BigIntegerField(default=0)
    url = models.CharField(max_length=100)
    show_text = models.CharField(max_length=100)
    author_pic = models.CharField(max_length=200, default="")
    tag_text = models.TextField(default='')
    tag_list = models.TextField(default='')
    python_tag = models.BooleanField(default=False)
    c1_tag = models.BooleanField(default=False)
    c2_tag = models.BooleanField(default=False)
    java_tag = models.BooleanField(default=False)
    javascript_tag = models.BooleanField(default=False)
    php_tag = models.BooleanField(default=False)
    sql_tag = models.BooleanField(default=False)
    else_tag = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    class Meta:
        indexes = [models.Index(fields=['date']), models.Index(fields=['hot']),
                   models.Index(fields=['title']), models.Index(fields=['article']),]


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_text = models.TextField()
    public_date = models.DateTimeField('date published')

    class Meta:
        indexes = [models.Index(fields=['public_date']), ]

