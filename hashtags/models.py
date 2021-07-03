from django.db import models
from blog.models import post

# Create your models here.
class HashTag(models.Model):
    tag = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_postss(self):
        return post.objects.filter(content__icontains="#" + self.tag)