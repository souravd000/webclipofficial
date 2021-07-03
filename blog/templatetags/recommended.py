from django import template
from django.contrib.auth import get_user_model
from blog.models import UserProfile

register = template.Library()


User = get_user_model()

@register.inclusion_tag("blog/snippets/recommended.html")
def recommended(user):
    if isinstance(user, User):
        qs = UserProfile.objects.recommended(user)
        return {"recommended": qs}