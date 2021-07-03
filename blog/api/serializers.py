from rest_framework import serializers
from accounts.api.serializers import UserDisplaySerializer


from blog.models import post

class ParentpostModelSerializer(serializers.ModelSerializer):
    author = UserDisplaySerializer()
    class Meta:
        model = post
        fields = [
            'author',
            'content',
            'likes',
        ]

class postModelSerializer(serializers.ModelSerializer):
    author = UserDisplaySerializer()
    parent = ParentpostModelSerializer()
    class Meta:
        model = post
        fields = [
            'author',
            'content',
            'parent',
            'likes',
        ]

    def get_did_like(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated():
                if user in obj.likes.all():
                    return True
        except:
            pass
        return False

    def get_likes(self, obj):
        return obj.likes.all().count()
