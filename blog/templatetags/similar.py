from django import template
from django.contrib.auth import get_user_model
from hashtags.models import HashTag


register = template.Library()


User = get_user_model()

@register.inclusion_tag("blog/snippets/similar.html")
def similar():
    psall = HashTag.objects.all()
    return {"psall": psall}