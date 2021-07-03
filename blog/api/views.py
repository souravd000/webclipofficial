from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import post
from .serializers import postModelSerializer


class postListAPIView(generics.ListAPIView):
    serializer_class = postModelSerializer

    def get_queryset(self):
        return post.objects.all()


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        post_qs = post.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_liked = post.objects.like_toggle(request.user, post_qs.first())
            return Response({'liked': is_liked})
        return Response({"message": message}, status=400)