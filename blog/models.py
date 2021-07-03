import re
from notifications.signals import notify
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.conf import settings
from .validators import validate_file_extension, validate_audiofile_extension
from PIL import Image





# Create your models here.
class postManager(models.Manager):
    def repost(self, author, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj


        obj = self.model(
                parent = og_parent,
                author = author,
                content = og_parent.content,
                image = og_parent.image,
                video = og_parent.video,
                audio = og_parent.audio
            )
        obj.save()
        return obj

    def delete(og_parent, *args, **kwargs):
        og_parent.image.delete()
        super().delete(*args, **kwargs)


    def like_toggle(self, user, post_obj):
        if user in post_obj.likes.all():
            is_liked = False
            post_obj.likes.remove(user)
        else:
            is_liked = True
            post_obj.likes.add(user)
        return is_liked

class post(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_pics', null=True, blank=True)
    video = models.FileField(upload_to='post_videos', null=True, blank=True, validators=[validate_file_extension])
    audio = models.FileField(upload_to='post_audios', null=True, blank=True, validators=[validate_audiofile_extension])
    audio_poster = models.ImageField(upload_to='audip_poster_pics', null=True, blank=True)
    audio_name = models.CharField(max_length=50, blank=True)
    audio_artist_name = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    haha = models.ManyToManyField(User, related_name='haha', blank=True)
    sad = models.ManyToManyField(User, related_name='sad', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    restrict_comments = models.BooleanField(default=False)
    restrict_repost = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, related_name='watchlist', blank=True)

    objects = postManager()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-date_posted', 'title']

    def get_absolute_url(self):
            return reverse ('blog-home')

    def total_likes(self):
        return self.likes.count()


def post_save_receiver(sender, instance, created, *args,**kwargs):
    if created and not instance.parent:
        user_regex = r'@(?P<username>[\w.@+-]+)'
        m = re.search(user_regex, instance.content)
        if m:
            try:
                recipient = User.objects.get(username=m.group('username'))
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass
            else:
                notify.send(instance.author, recipient=recipient, actor=instance.author, verb='mention you in a post', target=instance, nf_type='tagged_by_one_user')

post_save.connect(post_save_receiver, sender=post)
    #comment model#

class Comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    react = models.ManyToManyField(User, related_name='react', blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='comments-pics', null=True, blank=True)
    voice_record = models.FileField(upload_to='voice-comments', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '{}.{}'.format(self.post.title, str(self.user.username))


    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)


def comment_save_receiver(sender, instance, created, *args,**kwargs):
    if created :
        user_regex = r'@(?P<username>[\w.@+-]+)'
        m = re.search(user_regex, instance.content)
        if m:
            try:
                recipient = User.objects.get(username=m.group('username'))
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass
            else:
                notify.send(instance.user, recipient=recipient, actor=instance.user, verb='mention you in a post', target=instance.post, nf_type='tagged_by_one_user')

post_save.connect(comment_save_receiver, sender=Comment)


class UserProfileManager(models.Manager):
    use_for_related_fields = True
    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
           user_profile.following.remove(to_toggle_user)
           added = False
        else:
           user_profile.following.add(to_toggle_user)
           added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit_to=10):
        profile = user.owner
        following = profile.following.all()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs

class UserProfile(models.Model):
    user      = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')

    objects = UserProfileManager()

    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)


post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)

