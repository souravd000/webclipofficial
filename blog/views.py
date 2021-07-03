from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import post, Comment, UserProfile
from .forms import CommentForm
from .forms import UploadForm
from django.views import View
from django.db.models import BooleanField
from django.db.models import Q, Count
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from notifications.signals import notify
from django.template.loader import render_to_string
import datetime as dt
from django.views.decorators.cache import cache_page





# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    paginate_by = 30
    def get_queryset(self, *args, **kwargs):
        count_filter = Q(likes=self.request.user)
        like_case = Count('likes', filter=count_filter, output_field=BooleanField())
        im_following = self.request.user.owner.get_following()
        qs1 = post.objects.annotate(is_liked=like_case).filter(author__in=im_following)
        qs2 = post.objects.annotate(is_liked=like_case).filter(author=self.request.user)
        qs3 = post.objects.annotate(is_liked=like_case).all()

        qs = (qs1 | qs2 | qs3 ).distinct().order_by('?')
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
                )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        return context

class RepostView(View):
    def get(self, request, pk, *args, **kwargs):
        posts = get_object_or_404(post, pk=pk)
        if request.user.is_authenticated:
            new_post = post.objects.repost(request.user, posts)
            notify.send(self.request.user, recipient=posts.author, actor=self.request.user, verb='shared your post', target=posts, nf_type='shared_by_one_user')
            return HttpResponseRedirect("/")
        context = {
        'posts': post,
        'new_post': new_post,
        }

        return HttpResponseRedirect("/")




def post_detail(request, pk):
    posts = get_object_or_404(post, pk=pk)
    comments = Comment.objects.filter(post=posts, reply=None,).order_by('-timestamp')
    #post=posts is the above post details posts its mean post for the exact corresponding posts
    is_liked = False
    is_watchlist = False
    if posts.likes.filter(id=request.user.id).exists():
        is_liked = True

    if posts.watchlist.filter(pk=request.user.pk).exists():
        is_watchlist = True


    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None, request.FILES or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=posts, user=request.user, content=content, reply=comment_qs,)
            comment.save()
            notify.send(request.user, recipient=posts.author, actor=request.user, verb='comment in your post', target=posts, nf_type='comment_by_one_user')

    else:
        comment_form = CommentForm()
    context = {'posts':posts, 'comments':comments, 'comment_form':comment_form, 'is_liked': is_liked, 'is_watchlist': is_watchlist, 'total_likes': posts.total_likes(),}

    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_detail.html', context)


def like_post(request):
    # posts = get_object_or_404(Post, id=request.POST.get('post_id'))
    posts = get_object_or_404(post, id=request.POST.get('id'))
    # posts.likes.add for the particular posts and the post_id for the post itself its belongs to the post without any pk
    is_liked = False
    if posts.likes.filter(id=request.user.id).exists():
        posts.likes.remove(request.user)
        is_liked = False
    else:
        posts.likes.add(request.user)
        is_liked = True
        notify.send(request.user, recipient=posts.author, actor=request.user, verb='liked your post', target=posts, nf_type='liked_by_one_user')

    context = {'posts':posts, 'is_liked': is_liked, 'total_likes': posts.total_likes(),}



    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})

@login_required
def post_likes(request, pk):
    posts = get_object_or_404(post, pk=pk)
    post_likes = posts.likes.all()
    context = {'post_likes': post_likes,}

    return render(request, 'blog/post_likes.html', context)

@login_required
def most_likes(request):
    delta = dt.timedelta(days=10)
    posts = post.objects.filter(date_posted__gt=(dt.datetime.now() - delta)) \
        .annotate(like_count=Count('likes')).order_by('-like_count', '-date_posted')
    context = {'posts': posts}

    return render(request, 'blog/most_likes.html', context)

def post_watchlist(request, pk):
    posts = get_object_or_404(post, pk=pk)
    if posts.watchlist.filter(pk=request.user.pk).exists():
        posts.watchlist.remove(request.user)
    else:
        posts.watchlist.add(request.user)
    return HttpResponseRedirect(posts.get_absolute_url())

def post_watchlist_list(request):
    user = request.user
    all_watchlist = user.watchlist.all()
    context = {'all_watchlist': all_watchlist,}
    return render(request, 'blog/post_watchlist_list.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['content', 'image', 'video', 'restrict_comments', 'restrict_repost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def django_image_and_file_upload_ajax(request):
    if request.method == 'POST':
       form = UploadForm(request.POST, request.FILES)
       if form.is_valid():
           form.instance.author = request.user
           form.save()
           return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
       else:
           return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = UploadForm()
        return render(request, 'blog/upload.html', {'form': form})

class AudioCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['content', 'audio', 'audio_poster', 'audio_name', 'audio_artist_name', 'restrict_comments', 'restrict_repost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['content', 'restrict_comments', 'restrict_repost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    fields = ['content', 'image', 'video']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserDetailView(DetailView):
    template_name = 'blog/user_detail.html'
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, username__iexact=self.kwargs.get("username"))

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        context['recommended'] = UserProfile.objects.recommended(self.request.user)
        return context

class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)


        notify.send(self.request.user, recipient=toggle_user, actor=self.request.user, verb='followed you.', nf_type='followed_by_one_user')

        return redirect('user-posts', username=username)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    fields = ['content']
    success_url = '/'


class ErloListView(LoginRequiredMixin, ListView):
    paginate_by = 30
    def get_queryset(self, *args, **kwargs):
        count_filter = Q(likes=self.request.user)
        like_case = Count('likes', filter=count_filter, output_field=BooleanField())
        im_following = self.request.user.owner.get_following()
        qs = post.objects.annotate(is_liked=like_case).filter(author__in=im_following).order_by('-date_posted')

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ErloListView, self).get_context_data(*args, **kwargs)
        return context


def PhotoE(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def memegen(request):
    return render(request, 'blog/terms.html', {'title': 'Terms of Service'})

def privacypolicy(request):
    return render(request, 'blog/privacy.html', {'title': 'Privacy Policy'})

def helpcenter(request):
    return render(request, 'blog/help.html', {'title': 'Help Center'})

def contact(request):
    return render(request, 'blog/contact.html', {'title': 'Contact Information'})

def verificaacc(request):
    return render(request, 'blog/verify.html', {'title': 'Profile Verification'})

def contribacc(request):
    return render(request, 'blog/vip.html', {'title': 'Apply Popular Badge'})

def reportpost(request):
    return render(request, 'blog/reportpost.html', {'title': 'Report Post'})

def reportprofile(request):
    return render(request, 'blog/reportprofile.html', {'title': 'Report Profile'})

def accdlt(request):
    return render(request, 'blog/accdlt.html', {'title': 'Delete Account'})

def donation(request):
    return render(request, 'blog/donations.html')
