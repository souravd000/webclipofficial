from django import template
from django.contrib.auth import get_user_model
from blog.models import post
#from django import template
#from hashtags.models import HashTag
#from blog.models import post

#register = template.Library()

#@register.inclusion_tag("blog/snippets/suggest.html")
#def suggest():
        #hash = HashTag.objects.all()
        #return {'hash': hash}


register = template.Library()


User = get_user_model()

@register.inclusion_tag("blog/snippets/suggestaudio.html")
def suggestaudio(limit_to=10):
        postsall = post.objects.all().order_by("?")[:limit_to]
        return {"postsall": postsall}