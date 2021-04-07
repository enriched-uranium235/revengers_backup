import logging
import sys

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import InquiryForm, DiaryCreateForm, ExperiencesCreateForm, NoticeCreateForm, CommentCreateForm, DMForm, NewCommentForm, CommentCreateForm2
from .models import Avengers, Experiences, Comment, Notice, NoticeRead, Post, Good, Good2, Good3, Good4, Good5, Good6, Favorite, Favorite2, Report, Report2, Report3, Report4, Report5, Report6, Report7, Report1_1, Report2_1, Report3_1, Report4_1, Report5_1, Report6_1, Report7_1, BlackList, AllBlackList, AvengersLog, ExperiencesLog, DM, AttendanceRecord, AttendanceAllRecord, Comment2, Comment3
from accounts.models import Profile, Follow
from django.db.models import Count
from django.http import QueryDict, HttpResponse, JsonResponse
from xlsxwriter.workbook import Workbook
from io import BytesIO

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('avengers:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class DiaryListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'object_list'
    model = Avengers
    template_name = 'diary_list.html'
    paginate_by = 10

    def get_queryset(self):
        diaries = Avengers.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Avengers
    template_name = 'diary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['com_list'] = self.object.comment_set.filter(parent__isnull=True)
        post_id = self.kwargs['pk']
        context['comment_c'] = Comment.objects.filter(post__id=post_id).count()
        return context

# 表示回数を1増やす
def add_count(request, pk):
    post = Avengers.objects.get(pk=pk)
    post.views += 1
    post.save()
    return redirect('avengers:diary_detail', pk=post.pk)

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Avengers
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('avengers:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '新規投稿を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "新規投稿の作成に失敗しました。")
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Avengers
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('avengers:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '投稿内容を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "投稿内容の更新に失敗しました。")
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Avengers
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('avengers:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "投稿内容を削除しました。")
        return super().delete(request, *args, **kwargs)


# 経験談やアドバイスを投稿する
class ExperiencesListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'experience_list'
    model = Experiences
    template_name = 'experiences_list.html'
    paginate_by = 10

    def get_queryset(self):
        experiences = Experiences.objects.filter(user=self.request.user).order_by('-created_at')
        return experiences

class ExperiencesDetailView(LoginRequiredMixin, generic.DetailView):
    model = Experiences
    template_name = 'experiences_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['com_list'] = self.object.comment3_set.filter(parent__isnull=True)
        post_id = self.kwargs['pk']
        context['comment_c'] = Comment3.objects.filter(post_connected=post_id).count()
        return context

# 表示回数を1増やす
def add_count2(request, pk):
    post = Experiences.objects.get(pk=pk)
    post.views += 1
    post.save()
    return redirect('avengers:experiences_detail', pk=post.pk)

class ExperiencesCreateView(LoginRequiredMixin, generic.CreateView):
    model = Experiences
    template_name = 'experiences_create.html'
    form_class = ExperiencesCreateForm
    success_url = reverse_lazy('avengers:experiences_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '新規投稿を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "新規投稿の作成に失敗しました。")
        return super().form_invalid(form)

class ExperiencesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Experiences
    template_name = 'experiences_update.html'
    form_class = ExperiencesCreateForm

    def get_success_url(self):
        return reverse_lazy('avengers:experiences_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '投稿内容を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "投稿内容の更新に失敗しました。")
        return super().form_invalid(form)

class ExperiencesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Experiences
    template_name = 'experiences_delete.html'
    success_url = reverse_lazy('avengers:experiences_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "投稿内容を削除しました。")
        return super().delete(request, *args, **kwargs)


# 運営からの公式通知
class NoticeListView(LoginRequiredMixin, generic.ListView):
    model = Notice
    template_name = 'notice_from_management.html'
    context_object_name = 'notice_list'
    paginate_by = 100

    def get_queryset(self):
        notice = Notice.objects.all().order_by('-posted')
        return notice

# 通知作成
class NoticeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Notice
    template_name = 'notice_create.html'
    form_class = NoticeCreateForm
    success_url = reverse_lazy('avengers:notice_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '通知を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "通知の作成に失敗しました。")
        return super().form_invalid(form)

# 通知詳細確認
class NoticeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Notice
    template_name = 'notice_detail.html'

# 通知の既読処理
def noticeread(request, pk):
    user = request.user
    notice = Notice.objects.get(pk=pk)
    is_read = NoticeRead.objects.filter(user = request.user).filter(notice = pk).filter(is_read = True).count()
    if is_read > 0:
        return redirect('avengers:notice_detail', pk=pk)
    else:
        try:
            notice.read_list.append(request.user)
            notice.save()
        except:
            try:
                notice.read_list2.append(request.user)
                notice.save()
            except:
                try:
                    notice.read_list3.append(request.user)
                    notice.save()
                except:
                    try:
                        notice.read_list4.append(request.user)
                        notice.save()
                    except:
                        try:
                            notice.read_list5.append(request.user)
                            notice.save()
                        except:
                            messages.error('申し訳ありません、既読処理が正常に完了しませんでした。管理者側にお問い合わせください。')

        read = NoticeRead()
        read.user = user
        read.notice = notice
        read.is_read = True
        read.number = request.user.id
        read.save()
        return redirect('avengers:notice_detail', pk=pk)

# みんなの投稿
class AccuseListView(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_list.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.filter(show=True).order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿（動画のみ）
class AccuseListViewMovieOnly(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_video.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.filter(media1__exact='').filter(photo1__exact='').order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿(音声のみ)
class AccuseListViewSoundOnly(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_sound.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.filter(photo1__exact='').filter(media2__exact='').order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿(画像のみ)
class AccuseListViewPhotoOnly(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_photo.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.filter(media1__exact='').filter(media2__exact='').order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿(いいね降順)
class AccuseListViewGoodDescending(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_good_descending.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.all().order_by('-good_count')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿(いいね昇順)
class AccuseListViewGoodAscending(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_good_ascending.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.all().order_by('good_count')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿(投稿日時が古い順)
class AccuseListViewOld(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_old.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.all().order_by('created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

# みんなの投稿(投稿日時が新しい順)
class AccuseListViewNew(generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_new.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.all().order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            accuses = accuses.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(group__icontains=keyword)|Q(content__icontains=keyword))
        else:
            accuses = accuses
        return accuses

class AccuseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Avengers
    template_name = 'accuse_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['com_list'] = self.object.comment_set.filter(parent__isnull=True)
        post_id = self.kwargs['pk']
        context['comment_c'] = Comment.objects.filter(post__id=post_id).count()
        return context

# 関連リスト(被害投稿)
class AccuseReccomendView(LoginRequiredMixin, generic.ListView):
    model = Avengers
    template_name = 'accuse_reccomend.html'
    context_object_name = 'object_list2'

    def get_queryset(self):
        reccomend = Avengers.objects.all().order_by('-created_at')[:74]
        return reccomend


# みんなの投稿(Experience)
class PresentListView(generic.ListView):
    context_object_name = 'present_list'
    model = Experiences
    template_name = 'present_list.html'
    paginate_by = 40

    def get_queryset(self):
        present = Experiences.objects.all().order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            present = present.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(content__icontains=keyword))
        else:
            present = present
        return present

# みんなの投稿(いいね降順)
class PresentListViewGoodDescending(generic.ListView):
    context_object_name = 'present_list'
    model = Experiences
    template_name = 'present_good_descending.html'
    paginate_by = 40

    def get_queryset(self):
        experience = Experiences.objects.all().order_by('-good_count')
        keyword = self.request.GET.get('keyword')

        if keyword:
            experience = experience.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(content__icontains=keyword))
        else:
            experience = experience
        return experience

# みんなの投稿(いいね昇順experience)
class PresentListViewGoodAscending(generic.ListView):
    context_object_name = 'present_list'
    model = Experiences
    template_name = 'present_good_ascending.html'
    paginate_by = 40

    def get_queryset(self):
        experiences = Experiences.objects.all().order_by('good_count')
        keyword = self.request.GET.get('keyword')

        if keyword:
            experiences = experiences.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(content__icontains=keyword))
        else:
            experiences = experiences
        return experiences

# みんなの投稿(投稿日時が古い順)
class PresentListViewOld(generic.ListView):
    context_object_name = 'present_list'
    model = Experiences
    template_name = 'present_old.html'
    paginate_by = 40

    def get_queryset(self):
        experiences = Experiences.objects.all().order_by('created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            experiences = experiences.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(content__icontains=keyword))
        else:
            experiences = experiences
        return experiences

# みんなの投稿(投稿日時が新しい順)
class PresentListViewNew(generic.ListView):
    context_object_name = 'present_list'
    model = Experiences
    template_name = 'present_new.html'
    paginate_by = 40

    def get_queryset(self):
        experiences = Experiences.objects.all().order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            experiences = experiences.filter(Q(title__icontains=keyword)|Q(user__username__icontains=keyword)|Q(content__icontains=keyword))
        else:
            experiences = experiences
        return experiences

class PresentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Experiences
    template_name = 'present_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['com_list'] = self.object.comment3_set.filter(parent__isnull=True)
        post_id = self.kwargs['pk']
        context['comment_c'] = Comment3.objects.filter(post_connected=post_id).count()
        return context


class UserProfileView(generic.TemplateView):
    template_name = 'user_profile.html'

def comment_create(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Avengers, pk=post_pk)
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.user = User.objects.get(id=request.user.id)
        comment.created_at = timezone.now()
        comment.save()
        return redirect('avengers:accuse_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'comment_form.html', context)

def comment_create3(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Avengers, pk=post_pk)
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.user = User.objects.get(id=request.user.id)
        comment.created_at = timezone.now()
        comment.save()
        return redirect('avengers:diary_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'comment_form.html', context)

def reply_create(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.user = User.objects.get(id=request.user.id)
        reply.created_at = timezone.now()
        reply.save()
        return redirect('avengers:accuse_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'comment_form.html', context)

def reply_create2(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.user = User.objects.get(id=request.user.id)
        reply.created_at = timezone.now()
        reply.save()
        return redirect('avengers:diary_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'comment_form.html', context)

def comment_create2(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Experiences, pk=post_pk)
    form = CommentCreateForm2(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post_connected = post
        comment.author = User.objects.get(id=request.user.id)
        comment.date_posted = timezone.now()
        comment.save()
        return redirect('avengers:present_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'comment_form2.html', context)

def comment_create4(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Experiences, pk=post_pk)
    form = CommentCreateForm2(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post_connected = post
        comment.author = User.objects.get(id=request.user.id)
        comment.date_posted = timezone.now()
        comment.save()
        return redirect('avengers:experiences_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'comment_form2.html', context)

def reply_create3(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment3, pk=comment_pk)
    post = comment.post_connected
    form = CommentCreateForm2(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post_connected = post
        reply.author = User.objects.get(id=request.user.id)
        reply.date_posted = timezone.now()
        reply.save()
        return redirect('avengers:present_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'comment_form2.html', context)

def reply_create4(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment3, pk=comment_pk)
    post = comment.post_connected
    form = CommentCreateForm2(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post_connected = post
        reply.author = User.objects.get(id=request.user.id)
        reply.date_posted = timezone.now()
        reply.save()
        return redirect('avengers:experiences_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'comment_form2.html', context)


# Commentクラスに格納されたデータのリスト表示
class CommentView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = 'all_comments.html'
    context_object_name = 'all_comment'

    def get_queryset(self):
        comment = Comment.objects.all()
        keyword = self.request.GET.get('keyword')

        if keyword:
            comment = comment.filter(
                Q(user__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            comment = comment
        return comment

# Comment2クラスに格納されたデータのリスト表示
class CommentView2(LoginRequiredMixin, generic.ListView):
    model = Comment2
    template_name = 'all_comments2.html'
    context_object_name = 'all_comment2'

    def get_queryset(self):
        comment = Comment2.objects.all()
        keyword = self.request.GET.get('keyword')

        if keyword:
            comment = comment.filter(
                Q(user__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            comment = comment
        return comment

# Comment3クラスに格納されたデータのリスト表示
class CommentView3(LoginRequiredMixin, generic.ListView):
    model = Comment3
    template_name = 'all_comments3.html'
    context_object_name = 'all_comment3'

    def get_queryset(self):
        comment = Comment3.objects.all()
        keyword = self.request.GET.get('keyword')

        if keyword:
            comment = comment.filter(
                Q(user__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            comment = comment
        return comment


# twitter cloneを使ったコミュニティスレッド
def is_users(post_user, logged_user):
    return post_user == logged_user


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'mypage.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-author_count')

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author']).first())

        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        article = Post.objects.all().order_by('-date_posted')
        keyword = self.request.GET.get('keyword')

        if keyword:
            article = article.filter(
                Q(author__username__icontains=keyword) | Q(author__id__icontains=keyword) | Q(
                    content__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            article = article
        return article


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment2.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment2(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object(),
                              date_posted=timezone.now())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = '/community_room'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['content']
    template_name = 'post_new.html'
    success_url = '/community_room'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '新規スレッドを投稿しました。')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = '新規投稿'
        return data


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['content']
    template_name = 'post_new.html'
    success_url = '/community_room'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '投稿内容を更新しました。')
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = '投稿内容の編集'
        return data


class FollowsListView(generic.ListView):
    model = Follow
    template_name = 'follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(generic.ListView):
    model = Follow
    template_name = 'follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data


# 選択したフォローユーザーにDMを送る
def dm_to_follow(request, id):
    select = Follow.objects.get(user=request.user, follow_user=id)
    form = DMForm(request.POST or None)

    if request.method == 'POST':
        dm = form.save(commit=False)
        dm.owner = request.user
        dm.user = select.follow_user
        dm.save()
        messages.success(request, select.follow_user.username + 'さんにダイレクトメッセージを送りました!')
        return redirect('avengers:user-follows', username=request.user.username)

    context = {
        'form': form,
    }
    return render(request, 'dm.html', context)

# 選択したフォロワーにDMを送る
def dm_to_follower(request, id):
    select = Follow.objects.get(user=id, follow_user=request.user)
    form = DMForm(request.POST or None)

    if request.method == 'POST':
        dm = form.save(commit=False)
        dm.owner = request.user
        dm.user = select.user
        dm.save()
        messages.success(request, select.user.username + 'さんにダイレクトメッセージを送りました!')
        return redirect('avengers:user-followers', username=request.user.username)

    context = {
        'form': form,
    }
    return render(request, 'dm.html', context)

# DMを送ってきたユーザーに返信を送る
def dm_reply(request, id, pk):
    select = Follow.objects.get(user=id, follow_user=request.user)
    form = DMForm(request.POST or None)

    if request.method == 'POST':
        dm = form.save(commit=False)
        dm.owner = request.user
        dm.user = select.user
        dm.save()
        messages.success(request, select.user.username + 'さんに返信を送りました!')
        return redirect('avengers:dm_detail', pk=pk)

    context = {
        'form': form,
    }
    return render(request, 'dm.html', context)

# 送られたDMを一覧表示する
class DMListView(LoginRequiredMixin, generic.ListView):
    model = DM
    context_object_name = 'DM_list'
    paginated_by = 200
    template_name = 'dm_list.html'

    def get_queryset(self):
        dm = DM.objects.filter(user=self.request.user).order_by('-dm_created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            dm = dm.filter(Q(owner__username__icontains=keyword))
            messages.success(self.request, '{}さんからのダイレクトメッセージ'.format(keyword))
        else:
            dm = dm
        return dm

# 送られたDMを全件表示する(管理者専用)
class DMListAllView(LoginRequiredMixin, generic.ListView):
    model = DM
    context_object_name = 'DM_list'
    paginated_by = 200
    template_name = 'all_dm_list.html'

    def get_queryset(self):
        dm = DM.objects.all().order_by('-dm_created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            dm = dm.filter(Q(owner__username__icontains=keyword) | Q(owner__id__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}さんからのダイレクトメッセージ'.format(keyword))
        else:
            dm = dm
        return dm

# 送ったダイレクトメッセージを確認する
class DMSendListView(LoginRequiredMixin, generic.ListView):
    model = DM
    context_object_name = 'DM_list'
    paginated_by = 200
    template_name = 'dm_send_list.html'

    def get_queryset(self):
        dm = DM.objects.filter(owner=self.request.user).order_by('-dm_created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            dm = dm.filter(Q(user__username__icontains=keyword))
            messages.success(self.request, '{}さんへのダイレクトメッセージ'.format(keyword))
        else:
            dm = dm
        return dm

# 送ったダイレクトメッセージ全件を確認する(管理者用)
class DMAllSendListView(LoginRequiredMixin, generic.ListView):
    model = DM
    context_object_name = 'DM_list'
    paginated_by = 200
    template_name = 'dm_all_send_list.html'

    def get_queryset(self):
        dm = DM.objects.all().order_by('-dm_created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            dm = dm.filter(Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            dm = dm
        return dm

# DMの詳細を見る
class DMDetailView(LoginRequiredMixin, generic.DetailView):
    model = DM
    template_name = 'dm_detail.html'

# DMを既読にする処理
def dm_is_read(request, pk):
    dm = DM.objects.get(user=request.user, pk=pk)
    if dm.is_read == False:
        dm.is_read = True
        dm.save()
        return redirect('avengers:dm_detail', pk=pk)
    else:
        return redirect('avengers:dm_detail', pk=pk)


# 送ったDMの詳細を見る
class DMSendDetailView(LoginRequiredMixin, generic.DetailView):
    model = DM
    template_name = 'dm_send_detail.html'

# 送ったDMを削除する
class DMDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DM
    template_name = 'dm_delete.html'
    success_url = reverse_lazy('avengers:dm_send_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "ダイレクトメッセージを削除しました。")
        return super().delete(request, *args, **kwargs)


# goodボタンの処理(Post用)
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Post.objects.get(id=good_id)
    # 自分がAvengersにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
        .filter(post=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        # Messageのgood_countを1減らす
        good_msg.good_count -= 1
        good_msg.save()
        # Goodを消去
        like = Good.objects.filter(post=good_msg, owner=request.user)
        like.delete()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！を取り消しました。'
        }
        return JsonResponse(data=data)
    else:
        # Messageのgood_countを１増やす
        good_msg.good_count += 1
        good_msg.save()
        # Goodを作成し、設定して保存
        good = Good()
        good.owner = request.user
        good.post = good_msg
        good.save()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！しました。'
        }
        return JsonResponse(data=data)

# goodボタンの処理(Avengers投稿用)
def good2(request, good_id):
    # goodするMessageを取得
    good_msg = Avengers.objects.get(id=good_id)
    # 自分がAvengersにGoodした数を調べる
    is_good = Good2.objects.filter(owner=request.user) \
        .filter(avengers=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        # Messageのgood_countを1減らす
        good_msg.good_count -= 1
        good_msg.save()
        # Goodを消去
        like = Good2.objects.filter(avengers=good_msg, owner=request.user)
        like.delete()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！を取り消しました。'
        }
        return JsonResponse(data=data)
    else:
        # Messageのgood_countを１増やす
        good_msg.good_count += 1
        good_msg.save()
        # Good2を作成し、設定して保存
        good = Good2()
        good.owner = request.user
        good.avengers = good_msg
        good.save()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！しました。'
        }
        return JsonResponse(data=data)

# goodボタンの処理(Comment用)
def good3(request, good_id):
    # goodするCommentを取得
    good_msg = Comment.objects.get(id=good_id)
    # 自分がCommentにGoodした数を調べる
    is_good = Good3.objects.filter(owner=request.user) \
        .filter(comment=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        # Messageのgood_countを1減らす
        good_msg.good_count -= 1
        good_msg.save()
        # Goodを消去
        like = Good3.objects.filter(comment=good_msg, owner=request.user)
        like.delete()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！を取り消しました。'
        }
        return JsonResponse(data=data)
    else:
        # Messageのgood_countを１増やす
        good_msg.good_count += 1
        good_msg.save()
        # Good3を作成し、設定して保存
        good = Good3()
        good.owner = request.user
        good.comment = good_msg
        good.save()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！しました。'
        }
        return JsonResponse(data=data)

# goodボタンの処理(Comment2用)
def good4(request, good_id):
    # goodするCommentを取得
    good_msg = Comment2.objects.get(id=good_id)
    # 自分がCommentにGoodした数を調べる
    is_good = Good4.objects.filter(owner=request.user) \
        .filter(comment=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        # Messageのgood_countを1減らす
        good_msg.good_count -= 1
        good_msg.save()
        # Goodを消去
        like = Good4.objects.filter(comment=good_msg, owner=request.user)
        like.delete()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！を取り消しました。'
        }
        return JsonResponse(data=data)
    else:
        # Messageのgood_countを１増やす
        good_msg.good_count += 1
        good_msg.save()
        # Good4を作成し、設定して保存
        good = Good4()
        good.owner = request.user
        good.comment = good_msg
        good.save()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！しました。'
        }
        return JsonResponse(data=data)

# goodボタンの処理(Experience投稿用)
def good5(request, good_id):
    # goodするMessageを取得
    good_msg = Experiences.objects.get(id=good_id)
    # 自分がExperiencesにGoodした数を調べる
    is_good = Good5.objects.filter(owner=request.user) \
        .filter(experiences=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        # Messageのgood_countを1減らす
        good_msg.good_count -= 1
        good_msg.save()
        # Goodを消去
        like = Good5.objects.filter(experiences=good_msg, owner=request.user)
        like.delete()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！を取り消しました。'
        }
        return JsonResponse(data=data)
    else:
        # Messageのgood_countを１増やす
        good_msg.good_count += 1
        good_msg.save()
        # Good5を作成し、設定して保存
        good = Good5()
        good.owner = request.user
        good.experiences = good_msg
        good.save()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！しました。'
        }
        return JsonResponse(data=data)

# goodボタンの処理(Comment3用)
def good6(request, good_id):
    # goodするCommentを取得
    good_msg = Comment3.objects.get(id=good_id)
    # 自分がCommentにGoodした数を調べる
    is_good = Good6.objects.filter(owner=request.user) \
        .filter(comment=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        # Messageのgood_countを1減らす
        good_msg.good_count -= 1
        good_msg.save()
        # Goodを消去
        like = Good6.objects.filter(comment=good_msg, owner=request.user)
        like.delete()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！を取り消しました。'
        }
        return JsonResponse(data=data)
    else:
        # Messageのgood_countを１増やす
        good_msg.good_count += 1
        good_msg.save()
        # Good6を作成し、設定して保存
        good = Good6()
        good.owner = request.user
        good.comment = good_msg
        good.save()
        data = {
            'like': good_msg.good_count,
            'message': 'いいね！しました。'
        }
        return JsonResponse(data=data)

# ログを生成
def add_avengers_log(request, pk):
    post = get_object_or_404(Avengers, pk=pk)

    # 表示回数を1増やす
    count = Avengers.objects.get(pk=pk)
    count.views += 1
    count.save()

    # ログの作成
    log = AvengersLog.objects.filter(user=request.user).filter(pk=pk)
    log2 = AvengersLog()
    if log.exists:
        log.delete()
        log2.user = request.user
        log2.avengers = post
        log2.title = post.title
        log2.group = post.group
        log2.content = post.content
        log2.photo1 = post.photo1
        log2.media1 = post.media1
        log2.media2 = post.media2
        log2.number = post.pk
        log2.created_at = post.created_at
        log2.save()
    else:
        log2.user = request.user
        log2.avengers = post
        log2.title = post.title
        log2.group = post.group
        log2.content = post.content
        log2.photo1 = post.photo1
        log2.media1 = post.media1
        log2.media2 = post.media2
        log2.number = post.pk
        log2.created_at = post.created_at
        log2.save()

    return redirect('avengers:accuse_detail', pk=post.pk)

# ログの一覧表示
class AvengersLogView(LoginRequiredMixin, generic.ListView):
    model = AvengersLog
    template_name = 'avengers_log_list.html'
    context_object_name = 'avengers_log_list'

    def get_queryset(self):
        #登録済みのログを取得
        log = AvengersLog.objects.filter(user=self.request.user).order_by('-created_at')
        return log

# 閲覧履歴から登録された投稿へと飛ぶ
def see_avengers_log(request, pk):
    log = get_object_or_404(AvengersLog, pk=pk)
    number = log.number

    # 　カウントを1増やす
    post = get_object_or_404(Avengers, pk=log.number)
    count = Avengers.objects.get(pk=log.number)
    count.views += 1
    count.save()
    return redirect('avengers:accuse_detail', pk=number)


# ログを生成(experience)
def add_experiences_log(request, pk):
    post = get_object_or_404(Experiences, pk=pk)

    # 表示回数を1増やす
    count = Experiences.objects.get(pk=pk)
    count.views += 1
    count.save()

    # ログの作成
    log = ExperiencesLog.objects.filter(user=request.user).filter(pk=pk)
    log2 = ExperiencesLog()
    if log.exists:
        log.delete()
        log2.user = request.user
        log2.avengers = post
        log2.title = post.title
        log2.content = post.content
        log2.photo = post.photo
        log2.video = post.video
        log2.number = post.pk
        log2.created_at = post.created_at
        log2.save()
    else:
        log2.user = request.user
        log2.avengers = post
        log2.title = post.title
        log2.content = post.content
        log2.photo = post.photo
        log2.video = post.video
        log2.number = post.pk
        log2.created_at = post.created_at
        log2.save()

    return redirect('avengers:present_detail', pk=post.pk)

# ログの一覧表示
class ExperiencesLogView(LoginRequiredMixin, generic.ListView):
    model = ExperiencesLog
    template_name = 'experiences_log_list.html'
    context_object_name = 'experiences_log_list'

    def get_queryset(self):
        #登録済みのログを取得
        log = ExperiencesLog.objects.filter(user=self.request.user).order_by('-created_at')
        return log

# 閲覧履歴から登録された投稿へと飛ぶ
def see_experiences_log(request, pk):
    log = get_object_or_404(ExperiencesLog, pk=pk)
    number = log.number

    # 　カウントを1増やす
    post = get_object_or_404(Experiences, pk=log.number)
    count = Experiences.objects.get(pk=log.number)
    count.views += 1
    count.save()
    return redirect('avengers:present_detail', pk=number)


# お気に入り追加関数
def add_favorite(request, post_pk):
    # 追加する記事を取得
    post = get_object_or_404(Avengers, pk=post_pk)

    # ここからお気に入りの登録処理
    favorite = Favorite()
    favorite.owner = request.user
    favorite.favorite = post
    favorite.title = post.title
    favorite.group = post.group
    favorite.content = post.content
    favorite.photo1 = post.photo1
    favorite.media1 = post.media1
    favorite.media2 = post.media2
    favorite.number = post.id
    favorite.created_at = post.created_at
    favorite.updated_at = post.updated_at
    favorite.save()

    return JsonResponse({"favorite":""})

# お気に入りリスト
class FavoriteView(LoginRequiredMixin, generic.ListView):
    model = Favorite
    template_name = 'favorite_list.html'
    context_object_name = 'favorite_list'

    def get_queryset(self):
        #登録済みの投稿を取得
        favorite = Favorite.objects.filter(owner=self.request.user).order_by('-created_at')
        return favorite

def seefavorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)
    number = favorite.number

    count = Avengers.objects.get(pk=favorite.number)
    count.views += 1
    count.save()
    return redirect('avengers:accuse_detail', pk=number)

# お気に入りから削除
class FavoriteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Favorite
    template_name = 'favorite_delete.html'
    success_url = reverse_lazy('avengers:favorite')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "この投稿をお気に入りから削除しました。")
        return super().delete(request, *args, **kwargs)


# お気に入り追加関数(experience)
def add_favorite2(request, post_pk):
    # 追加する記事を取得
    post = get_object_or_404(Experiences, pk=post_pk)

    # ここからお気に入りの登録処理
    favorite = Favorite2()
    favorite.owner = request.user
    favorite.favorite = post
    favorite.title = post.title
    favorite.content = post.content
    favorite.photo = post.photo
    favorite.video = post.video
    favorite.number = post.id
    favorite.created_at = post.created_at
    favorite.updated_at = post.updated_at
    favorite.save()

    return JsonResponse({"favorite":""})

# お気に入りリスト
class FavoriteView2(LoginRequiredMixin, generic.ListView):
    model = Favorite2
    template_name = 'favorite_list2.html'
    context_object_name = 'favorite_list2'

    def get_queryset(self):
        #登録済みの投稿を取得
        favorite = Favorite2.objects.filter(owner=self.request.user).order_by('-created_at')
        return favorite

def seefavorite2(request, pk):
    favorite = get_object_or_404(Favorite2, pk=pk)
    number = favorite.number

    count = Experiences.objects.get(pk=favorite.number)
    count.views += 1
    count.save()
    return redirect('avengers:present_detail', pk=number)

# お気に入りから削除
class FavoriteDeleteView2(LoginRequiredMixin, generic.DeleteView):
    model = Favorite
    template_name = 'favorite_delete2.html'
    success_url = reverse_lazy('avengers:favorite2')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "この投稿をお気に入りから削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能1(Avengers投稿用)
def blacksubscribe1(request, subscribe_id):
    # Avengersを取得
    post = Avengers.objects.get(pk=subscribe_id)
    # Reportクラスを取得
    rep = Report1_1.objects.filter(pk=subscribe_id).filter(owner=request.user).count()
    if rep > 0:
        return JsonResponse({"report":""})

    else:
        black = BlackList()
        black.user = post.user
        black.save()

        # ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = post.user.username
        bl.user_id = post.user.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report()
        report.user = post.user.username
        report.user_id = post.user.id
        report.report = post
        report.title = post.title
        report.group = post.group
        report.content = post.content
        report.photo1 = post.photo1
        report.media1 = post.media1
        report.media2 = post.media2
        report.number = post.id
        report.created_at = post.created_at
        report.save()

        # 永久保存用DBに情報を登録
        r = Report1_1()
        r.user = post.user.username
        r.user_id = post.user.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.title = post.title
        r.group = post.group
        r.content = post.content
        r.photo1 = post.photo1
        r.media1 = post.media1
        r.media2 = post.media2
        r.number = post.id
        r.created_at = str(post.created_at)
        r.reported_date = str(timezone.now())
        r.save()
        # メッセージを設定
        return JsonResponse({"report": ""})

# 通報リスト(Avengers投稿)
class ReportView(LoginRequiredMixin, generic.ListView):
    model = Report
    template_name = 'report.html'
    context_object_name = 'report_list1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report.objects.all().order_by('-created_at')
        return report

# リストから通報された投稿へと飛ぶ
def seereport(request, pk):
    report = get_object_or_404(Report, pk=pk)
    number = report.number
    return redirect('avengers:accuse_detail', pk=number)

# 無害な投稿をリストから削除
class ReportDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Report
    template_name = 'report_delete.html'
    success_url = reverse_lazy('avengers:report-list01')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "この投稿を通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)

# 通報のあった投稿をアプリ内で削除
class AccuseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Avengers
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('avengers:report-list01')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "通報された投稿を削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能2(Comment,Reply用)
def blacksubscribe2(request, pk, comment_pk):
    # Avengersを取得
    post = get_object_or_404(Avengers, pk=pk)
    # Reportクラスを取得
    rep = Report2_1.objects.filter(pk=pk).filter(owner=request.user).count()
    # Commentを取得
    comment = get_object_or_404(Comment, pk=comment_pk)
    if rep > 0:
        return JsonResponse({"report": ""})

    else:
        # ブラックリストを取得
        black = BlackList()
        black.user = comment.user
        black.save()

        # ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = comment.user.username
        bl.user_id = comment.user.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report2()
        report.user = comment.user.username
        report.user_id = comment.user.id
        report.report = comment
        report.content = comment.content
        report.number1 = post.pk
        report.number2 = comment.pk
        report.save()

        # 通報された投稿を永久保存する処理
        r = Report2_1()
        r.user = comment.user.username
        r.user_id = comment.user.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.content = comment.content
        r.number1 = post.pk
        r.number2 = comment.pk
        r.created_at = str(comment.created_at)
        r.reported_at = str(timezone.now())
        r.save()
        # メッセージを設定
        return JsonResponse({"report": ""})

# 通報リスト2(Comment,Reply投稿)
class ReportView2(LoginRequiredMixin, generic.ListView):
    model = Report2
    template_name = 'report2.html'
    context_object_name = 'report_list2'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report2.objects.all()
        return report

# リストから通報されたコメントのある投稿へと飛ぶ
def seereport2(request, pk):
    report = get_object_or_404(Report2, pk=pk)
    number = report.number1
    return redirect('avengers:accuse_detail', pk=number)

# 無害なコメントをリストから削除
class ReportDeleteView2(LoginRequiredMixin, generic.DeleteView):
    model = Report2
    template_name = 'report_delete2.html'
    success_url = reverse_lazy('avengers:report-list02')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "このコメントを通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)

# 通報のあったコメントをアプリ内で削除
class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('avengers:report-list02')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "通報された投稿を削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能3(スレッド用)
def blacksubscribe3(request, pk):
    # Postを取得
    post = get_object_or_404(Post, pk=pk)
    # Reportクラスを取得
    rep = Report3_1.objects.filter(pk=pk).filter(owner=request.user).count()

    if rep > 0:
        return JsonResponse({"report": ""})

    else:
        # ブラックリストを取得
        black = BlackList()
        black.user = post.author
        black.save()

        #ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = post.author.username
        bl.user_id = post.author.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report3()
        report.user = post.author.username
        report.user_id = post.author.id
        report.report = post
        report.content = post.content
        report.number = post.pk
        report.save()

        # 通報されたスレッドを永久保存する処理
        r = Report3_1()
        r.user = post.author.username
        r.user_id = post.author.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.content = post.content
        r.number = post.pk
        r.created_at = str(post.date_posted)
        r.reported_at = str(timezone.now())
        r.save()
        return JsonResponse({"report": ""})

# 通報リスト3(スレッド投稿)
class ReportView3(LoginRequiredMixin, generic.ListView):
    model = Report3
    template_name = 'report3.html'
    context_object_name = 'report_list3'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report3.objects.all()
        return report

# 無害なスレッドをリストから削除
class ReportDeleteView3(LoginRequiredMixin, generic.DeleteView):
    model = Report3
    template_name = 'report_delete3.html'
    success_url = reverse_lazy('avengers:report-list03')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "このスレッドを通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)

# 通報のあったスレッドをアプリ内で削除
class ThreadDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('avengers:report-list03')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "通報された投稿を削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能4(DM用)
def blacksubscribe4(request, pk):
    # Postを取得
    dm = get_object_or_404(DM, pk=pk)
    # Reportクラスを取得
    rep = Report4_1.objects.filter(pk=pk).filter(owner=request.user).count()

    if rep > 0:
        return JsonResponse({"report": ""})

    else:
        # ブラックリストを取得
        black = BlackList()
        black.user = dm.owner
        black.save()

        # ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = dm.owner.username
        bl.user_id = dm.owner.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report4()
        report.user = dm.owner.username
        report.user_id = dm.owner.id
        report.report = dm
        report.content = dm.content
        report.number = dm.pk
        report.save()

        # ここから通報されたDMの永久保存処理
        r = Report4_1()
        r.user = dm.owner.username
        r.user_id = dm.owner.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.content = dm.content
        r.number = dm.pk
        r.created_at = str(dm.dm_created_at)
        r.reported_at = str(timezone.now())
        r.save()
        return JsonResponse({"report": ""})

# 通報リスト4(DM投稿)
class ReportView4(LoginRequiredMixin, generic.ListView):
    model = Report4
    template_name = 'report4.html'
    context_object_name = 'report_list4'

    def get_queryset(self):
        #登録済みのDMを取得
        report = Report4.objects.all()
        return report

# 無害なDMをリストから削除
class ReportDeleteView4(LoginRequiredMixin, generic.DeleteView):
    model = Report4
    template_name = 'report_delete4.html'
    success_url = reverse_lazy('avengers:report-list04')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "このスレッドを通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能5(Comment2用)
def blacksubscribe5(request, pk, comment_pk):
    # Postを取得
    post = get_object_or_404(Post, pk=pk)
    # Commentを取得
    comment = get_object_or_404(Comment2, pk=comment_pk)
    # Reportクラスを取得
    rep = Report5_1.objects.filter(pk=pk).filter(owner=request.user).count()

    if rep > 0:
        return JsonResponse({"report": ""})

    else:
        # ブラックリストを取得
        black = BlackList()
        black.user = comment.author
        black.save()

        # ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = comment.author.username
        bl.user_id = comment.author.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report5()
        report.user = comment.author.username
        report.user_id = comment.author.id
        report.report = comment
        report.content = comment.content
        report.number = comment.pk
        report.save()

        # 通報された投稿を永久保存する処理
        r = Report5_1()
        r.user = comment.author.username
        r.user_id = comment.author.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.content = comment.content
        r.report = comment
        r.number = comment.pk
        r.created_at = str(comment.date_posted)
        r.reported_at = str(timezone.now())
        r.save()
        return JsonResponse({"report": ""})

# 通報リスト2(Comment2投稿)
class ReportView5(LoginRequiredMixin, generic.ListView):
    model = Report5
    template_name = 'report5.html'
    context_object_name = 'report_list5'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report5.objects.all()
        return report

# 無害なコメントをリストから削除
class ReportDeleteView5(LoginRequiredMixin, generic.DeleteView):
    model = Report5
    template_name = 'report_delete5.html'
    success_url = reverse_lazy('avengers:report-list05')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "このコメントを通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)

# 通報のあったコメントをアプリ内で削除
class CommentDeleteView2(LoginRequiredMixin, generic.DeleteView):
    model = Comment2
    template_name = 'comment_delete2.html'
    success_url = reverse_lazy('avengers:report-list05')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "通報された投稿を削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能6(Experiences投稿用)
def blacksubscribe6(request, subscribe_id):
    # Experiencesを取得
    post = Experiences.objects.get(pk=subscribe_id)
    # Reportクラスを取得
    rep = Report6_1.objects.filter(pk=subscribe_id).filter(owner=request.user).count()
    if rep > 0:
        return JsonResponse({"report":""})

    else:
        black = BlackList()
        black.user = post.user
        black.save()

        # ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = post.user.username
        bl.user_id = post.user.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report6()
        report.user = post.user.username
        report.user_id = post.user.id
        report.report = post
        report.title = post.title
        report.content = post.content
        report.photo = post.photo
        report.video = post.video
        report.number = post.id
        report.created_at = post.created_at
        report.save()

        # 永久保存用DBに情報を登録
        r = Report6_1()
        r.user = post.user.username
        r.user_id = post.user.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.report = post
        r.title = post.title
        r.content = post.content
        r.photo = post.photo
        r.video = post.video
        r.number = post.id
        r.created_at = str(post.created_at)
        r.reported_at = str(timezone.now())
        r.save()
        # メッセージを設定
        return JsonResponse({"report":""})

# 通報リスト(Avengers投稿)
class ReportView6(LoginRequiredMixin, generic.ListView):
    model = Report6
    template_name = 'report6.html'
    context_object_name = 'report_list6'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report6.objects.all().order_by('-created_at')
        return report

# リストから通報された投稿へと飛ぶ
def seereport3(request, pk):
    report = get_object_or_404(Report6, pk=pk)
    number = report.number
    return redirect('avengers:present_detail', pk=number)

# 無害な投稿をリストから削除
class ReportDeleteView6(LoginRequiredMixin, generic.DeleteView):
    model = Report6
    template_name = 'report_delete6.html'
    success_url = reverse_lazy('avengers:report-list06')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "この投稿を通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)

# 通報のあった投稿をアプリ内で削除
class PresentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Experiences
    template_name = 'experiences_delete.html'
    success_url = reverse_lazy('avengers:report-list06')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "通報された投稿を削除しました。")
        return super().delete(request, *args, **kwargs)


# 通報機能7(Comment3用)
def blacksubscribe7(request, pk, comment_pk):
    # Postを取得
    post = get_object_or_404(Experiences, pk=pk)
    # Commentを取得
    comment = get_object_or_404(Comment3, pk=comment_pk)
    # Reportクラスを取得
    rep = Report7_1.objects.filter(pk=pk).filter(owner=request.user).count()

    if rep > 0:
        return JsonResponse({"report": ""})

    else:
        # ブラックリストを取得
        black = BlackList()
        black.user = comment.author
        black.save()

        # ブラックリスト(永久保存)に登録
        bl = AllBlackList()
        bl.user = comment.author.username
        bl.user_id = comment.author.id
        bl.save()

        # ここから通報された投稿の登録処理
        report = Report7()
        report.user = comment.author.username
        report.user_id = comment.author.id
        report.report = comment
        report.content = comment.content
        report.number = comment.pk
        report.save()

        # 通報された投稿を永久保存する処理
        r = Report7_1()
        r.user = comment.author.username
        r.user_id = comment.author.id
        r.owner = request.user.username
        r.owner_id = request.user.id
        r.content = comment.content
        r.report = comment
        r.number = comment.pk
        r.created_at = str(comment.date_posted)
        r.reported_at = str(timezone.now())
        r.save()
        return JsonResponse({"report": ""})

# 通報リスト7(Comment3投稿)
class ReportView7(LoginRequiredMixin, generic.ListView):
    model = Report7
    template_name = 'report7.html'
    context_object_name = 'report_list7'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report7.objects.all()
        return report

# 無害なコメントをリストから削除
class ReportDeleteView7(LoginRequiredMixin, generic.DeleteView):
    model = Report7
    template_name = 'report_delete7.html'
    success_url = reverse_lazy('avengers:report-list07')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "このコメントを通報リストから削除しました。")
        return super().delete(request, *args, **kwargs)

# 通報のあったコメントをアプリ内で削除
class CommentDeleteView3(LoginRequiredMixin, generic.DeleteView):
    model = Comment3
    template_name = 'comment_delete3.html'
    success_url = reverse_lazy('avengers:report-list07')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "通報された投稿を削除しました。")
        return super().delete(request, *args, **kwargs)


# 永久保存版の通報データの表示1
class EternalReportView(LoginRequiredMixin, generic.ListView):
    model = Report1_1
    template_name = 'eternal_report.html'
    context_object_name = 'report_list1_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report1_1.objects.all().order_by('-reported_date')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(group__icontains=keyword) | Q(created_at__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report

# 永久保存版の通報データの表示2
class EternalReportView2(LoginRequiredMixin, generic.ListView):
    model = Report2_1
    template_name = 'eternal_report2.html'
    context_object_name = 'report_list2_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report2_1.objects.all().order_by('-reported_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report

# 永久保存版の通報データの表示3
class EternalReportView3(LoginRequiredMixin, generic.ListView):
    model = Report3_1
    template_name = 'eternal_report3.html'
    context_object_name = 'report_list3_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report3_1.objects.all().order_by('-reported_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report

# 永久保存版の通報データの表示4
class EternalReportView4(LoginRequiredMixin, generic.ListView):
    model = Report4_1
    template_name = 'eternal_report4.html'
    context_object_name = 'report_list4_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report4_1.objects.all().order_by('-reported_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report

# 永久保存版の通報データの表示5
class EternalReportView5(LoginRequiredMixin, generic.ListView):
    model = Report5_1
    template_name = 'eternal_report5.html'
    context_object_name = 'report_list5_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report5_1.objects.all().order_by('-reported_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report

# 永久保存版の通報データの表示6
class EternalReportView6(LoginRequiredMixin, generic.ListView):
    model = Report6_1
    template_name = 'eternal_report6.html'
    context_object_name = 'report_list6_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report6_1.objects.all().order_by('-reported_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(created_at__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report

# 永久保存版の通報データの表示7
class EternalReportView7(LoginRequiredMixin, generic.ListView):
    model = Report7_1
    template_name = 'eternal_report7.html'
    context_object_name = 'report_list7_1'

    def get_queryset(self):
        #登録済みの投稿を取得
        report = Report7_1.objects.all().order_by('-reported_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            report = report.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(owner__username__icontains=keyword) | Q(content__icontains=keyword))
            messages.success(self.request, '{}での検索結果'.format(keyword))
        else:
            report = report
        return report


# ブラックリストの一覧表示
class BlackListView(LoginRequiredMixin, generic.ListView):
    model = BlackList
    template_name = 'black_list.html'
    context_object_name = 'black_list'

    def get_queryset(self):
        bl = BlackList.objects.all()
        keyword = self.request.GET.get('keyword')

        if keyword:
            bl = bl.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            bl = bl
        return bl

# 全てのブラックリストの一覧表示
class AllBlackListView(LoginRequiredMixin, generic.ListView):
    model = AllBlackList
    template_name = 'all_black_list.html'
    context_object_name = 'black_list'

    def get_queryset(self):
        bl = AllBlackList.objects.all()
        keyword = self.request.GET.get('keyword')

        if keyword:
            bl = bl.filter(
                Q(user__icontains=keyword) | Q(user_id__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            bl = bl
        return bl


# ログイン・ログアウトの履歴の確認
class AttendanceListView(LoginRequiredMixin, generic.ListView):
    model = AttendanceRecord
    template_name = 'log_in_out.html'
    context_object_name = 'user_log_list'

    def get_queryset(self):
        log = AttendanceRecord.objects.all().order_by('-login_time')
        keyword = self.request.GET.get('keyword')

        if keyword:
            log = log.filter(
                Q(user__username__icontains=keyword) | Q(user__id__icontains=keyword) | Q(login_time__icontains=keyword) | Q(logout_time__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            log = log
        return log

# 削除済みユーザーを含む全てのユーザーのログ
class AttendanceAllListView(LoginRequiredMixin, generic.ListView):
    model = AttendanceAllRecord
    template_name = 'all_log_in_out.html'
    context_object_name = 'all_log_in_out'

    def get_queryset(self):
        log = AttendanceAllRecord.objects.all().order_by('-login_time')
        keyword = self.request.GET.get('keyword')

        if keyword:
            log = log.filter(
                Q(user__icontains=keyword) | Q(user_id__icontains=keyword) | Q(user_email__icontains=keyword) | Q(login_time__icontains=keyword) | Q(logout_time__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        else:
            log = log
        return log

# 通報されたAvengers情報をexcelに出力
def excel_export(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('Vengeancersレポート履歴')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:A', 10)
    sheet.set_column('B:E', 20)
    sheet.set_column('F:F', 50)
    sheet.set_column('G:H', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'ユーザーID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者')
    sheet.write(0, 4, 'タイトル')
    sheet.write(0, 5, '詳細')
    sheet.write(0, 6, '投稿日時')
    sheet.write(0, 7, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report1_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.title)
        sheet.write(row_num, 5, data.content)
        sheet.write(row_num, 6, data.created_at)
        sheet.write(row_num, 7, data.reported_date)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=vengeancers_all_report.xlsx"

    return response

# 通報されたコメント、リプライ情報をexcelに出力
def excel_export2(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('通報されたコメント、返信')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:D', 20)
    sheet.set_column('E:E', 50)
    sheet.set_column('F:G', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'コメント投稿者ID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者名')
    sheet.write(0, 4, 'コメント内容')
    sheet.write(0, 5, '投稿日時')
    sheet.write(0, 6, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report2_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.content)
        sheet.write(row_num, 5, data.created_at)
        sheet.write(row_num, 6, data.reported_at)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=comment_report.xlsx"

    return response

# 通報されたスレッド情報をexcelに出力
def excel_export3(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('通報されたスレッド')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:D', 20)
    sheet.set_column('E:E', 50)
    sheet.set_column('F:G', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, '投稿者ID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者名')
    sheet.write(0, 4, 'スレッド内容')
    sheet.write(0, 5, '投稿日時')
    sheet.write(0, 6, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report3_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.content)
        sheet.write(row_num, 5, data.created_at)
        sheet.write(row_num, 6, data.reported_at)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=post_report.xlsx"

    return response

# 通報されたスレッド情報をexcelに出力
def excel_export4(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('通報されたDM')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:D', 20)
    sheet.set_column('E:E', 50)
    sheet.set_column('F:G', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'DM投稿者ID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者名')
    sheet.write(0, 4, 'DM内容')
    sheet.write(0, 5, '投稿日時')
    sheet.write(0, 6, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report4_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.content)
        sheet.write(row_num, 5, data.created_at)
        sheet.write(row_num, 6, data.reported_at)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=dm_report.xlsx"

    return response

# ブラックリスト情報をexcelに出力
def excel_export5(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('ブラックリスト')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:A', 10)
    sheet.set_column('B:B', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'ユーザーID')
    sheet.write(0, 1, 'ユーザー名')

    # ここは取得するデータに合わせて取得してください。
    db_data = AllBlackList.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=black_list.xlsx"

    return response

# ログ情報をexcelに出力
def excel_export6(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('ログインログアウト履歴')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:A', 10)
    sheet.set_column('B:B', 20)
    sheet.set_column('C:C', 30)
    sheet.set_column('D:E', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'ユーザーID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, 'e-mailアドレス')
    sheet.write(0, 3, 'ログイン')
    sheet.write(0, 4, 'ログアウト')

    # ここは取得するデータに合わせて取得してください。
    db_data = AttendanceAllRecord.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.user_email)
        sheet.write(row_num, 3, data.login_time)
        sheet.write(row_num, 4, data.logout_time)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=login_logout.xlsx"

    return response

# 通報されたコメント情報をexcelに出力
def excel_export7(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('通報されたコメント、返信')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:D', 20)
    sheet.set_column('E:E', 50)
    sheet.set_column('F:G', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'コメント投稿者ID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者名')
    sheet.write(0, 4, 'コメント内容')
    sheet.write(0, 5, '投稿日時')
    sheet.write(0, 6, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report5_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.content)
        sheet.write(row_num, 5, data.created_at)
        sheet.write(row_num, 6, data.reported_at)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=comment2_report.xlsx"

    return response

# 通報されたExperiences情報をexcelに出力
def excel_export8(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('Presentレポート履歴')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:A', 10)
    sheet.set_column('B:E', 20)
    sheet.set_column('F:F', 50)
    sheet.set_column('G:H', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'ユーザーID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者')
    sheet.write(0, 4, 'タイトル')
    sheet.write(0, 5, '詳細')
    sheet.write(0, 6, '投稿日時')
    sheet.write(0, 7, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report6_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.title)
        sheet.write(row_num, 5, data.content)
        sheet.write(row_num, 6, data.created_at)
        sheet.write(row_num, 7, data.reported_at)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=vengeancers_experiences_all_report.xlsx"

    return response

# 通報されたコメント情報をexcelに出力
def excel_export9(request):
    output = BytesIO()

    book = Workbook(output, options={'remove_timezone': True})
    sheet = book.add_worksheet('通報されたコメント、返信')

    # A列は15、B〜E列は20で幅を設定しています。自由に設定してください。
    sheet.set_column('A:D', 20)
    sheet.set_column('E:E', 50)
    sheet.set_column('F:G', 20)

    # ヘッダー。第一引数が行、第二引数が列を表しています。
    sheet.write(0, 0, 'コメント投稿者ID')
    sheet.write(0, 1, 'ユーザー名')
    sheet.write(0, 2, '通報者ID')
    sheet.write(0, 3, '通報者名')
    sheet.write(0, 4, 'コメント内容')
    sheet.write(0, 5, '投稿日時')
    sheet.write(0, 6, '通報日時')

    # ここは取得するデータに合わせて取得してください。
    db_data = Report7_1.objects.all().order_by('id')

    row_num = 1
    for data in db_data:
        sheet.write(row_num, 0, data.user_id)
        sheet.write(row_num, 1, data.user)
        sheet.write(row_num, 2, data.owner_id)
        sheet.write(row_num, 3, data.owner)
        sheet.write(row_num, 4, data.content)
        sheet.write(row_num, 5, data.created_at)
        sheet.write(row_num, 6, data.reported_at)

        row_num += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=comment3_report.xlsx"

    return response


#退会機能
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser

class UserDeleteView(OnlyYouMixin, generic.DeleteView):
    template_name = "delete.html"
    success_url = reverse_lazy("avengers:delete_confirm")
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

class DeleteConfirmView(generic.TemplateView):
    template_name = 'delete_complete.html'

#メンタルチェック
class MentalCheckView(generic.TemplateView):
    template_name = 'mental_check.html'

#都道府県情報から近くの専門家(弁護士・心療内科・労基署・カウンセラー)を探す
class SearchLawyer(generic.TemplateView):
    template_name = 'search_expert.html'

#ユーザーマニュアルを見る
class UserManualView(generic.TemplateView):
    template_name = 'user_manual.html'


# ここから先各マニュアルのテンプレート
# PC
# トップページ(ログイン前,PC)
class UserManualPCIndex(generic.TemplateView):
    template_name = 'manual/user_manual_pc_top_nav_before_login.html'
# お問い合わせ(ログイン前,PC)
class UserManualPCContact(generic.TemplateView):
    template_name = 'manual/user_manual_pc_contact_before_login.html'
# メンタルチェック(ログイン前,PC)
class UserManualPCMentalCheck(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mentalcheck_before_login.html'
# 専門家を探す(ログイン前,PC)
class UserManualPCSearchLawyer(generic.TemplateView):
    template_name = 'manual/user_manual_pc_searchlawyer_before_login.html'
# サインアップ(PC)
class UserManualPCSignUp(generic.TemplateView):
    template_name = 'manual/user_manual_pc_signup.html'
# ログイン(PC)
class UserManualPCLogIn(generic.TemplateView):
    template_name = 'manual/user_manual_pc_login.html'
# トップページ(ログイン後,PC)
class UserManualPCIndex2(generic.TemplateView):
    template_name = 'manual/user_manual_pc_top_nav_after_login.html'
# お問い合わせ(ログイン後,PC)
class UserManualPCContact2(generic.TemplateView):
    template_name = 'manual/user_manual_pc_contact_after_login.html'
# メンタルチェック(ログイン後,PC)
class UserManualPCMentalCheck2(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mentalcheck_after_login.html'
# 専門家を探す(ログイン後,PC)
class UserManualPCSearchLawyer2(generic.TemplateView):
    template_name = 'manual/user_manual_pc_searchlawyer_after_login.html'
# MyPage(画面説明,PC)
class UserManualPCMyPage(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage.html'
# MyPage 表示履歴(PC)
class UserManualPCMyPageLog(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_log.html'
# MyPage 新規投稿(PC)
class UserManualPCMyPageCreate(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_create.html'
# MyPage お気に入りリスト(PC)
class UserManualPCMyPageFavorite(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_favorite.html'
# MyPage 詳細(PC)
class UserManualPCMyPageDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_detail.html'
# MyPage 投稿更新(PC)
class UserManualPCMyPageUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_detail_update.html'
# MyPage 投稿削除(PC)
class UserManualPCMyPageDelete(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_delete.html'
# MyPage 返信作成(PC)
class UserManualPCMyPageReply(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_detail_reply.html'
# MyPage いいね!(PC)
class UserManualPCMyPageGood(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_comment_good.html'
# MyPage 通報(PC)
class UserManualPCMyPageReport(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_report.html'
# MyPage フォロー(PC)
class UserManualPCMyPageFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_mypage_follow.html'
# Everyone'sPost 画面説明(PC)
class UserManualPCEveryonesPost(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost.html'
# Everyone'sPost いいね(PC)
class UserManualPCEveryonesPostGood(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_good.html'
# Everyone'sPost 詳細(PC)
class UserManualPCEveryonesPostDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail.html'
# Everyone'sPost 記事投稿者フォロー(PC)
class UserManualPCEveryonesPostDetailFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_follow.html'
# Everyone'sPost 記事にコメント(PC)
class UserManualPCEveryonesPostDetailComment(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_comment.html'
# Everyone'sPost 詳細いいね!(PC)
class UserManualPCEveryonesPostDetailGood(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_good.html'
# Everyone'sPost 詳細お気に入り(PC)
class UserManualPCEveryonesPostDetailFavorite(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_favorite.html'
# Everyone'sPost 詳細通報(PC)
class UserManualPCEveryonesPostDetailReport(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_report.html'
# Everyone'sPost 詳細返信(PC)
class UserManualPCEveryonesPostDetailReply(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_reply.html'
# Everyone'sPost 詳細コメントいいね!(PC)
class UserManualPCEveryonesPostDetailCommentGood(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_comment_good.html'
# Everyone'sPost 詳細コメント通報(PC)
class UserManualPCEveryonesPostDetailCommentReport(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_comment_report.html'
# Everyone'sPost 詳細コメントフォロー(PC)
class UserManualPCEveryonesPostDetailCommentFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_everyonespost_detail_comment_follow.html'
# CommunityRoom(PC)
class UserManualPCCommunityRoom(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom.html'
# CommunityRoom 再読み込み(PC)
class UserManualPCCommunityRoomUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_update.html'
# CommunityRoom あなたの投稿(PC)
class UserManualPCCommunityRoomYourPost(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_yourpost.html'
# CommunityRoom あなたの投稿更新(PC)
class UserManualPCCommunityRoomYourPostUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_yourpost_update.html'
# CommunityRoom あなたの投稿削除(PC)
class UserManualPCCommunityRoomYourPostDelete(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_yourpost_delete.html'
# CommunityRoom 新規投稿(PC)
class UserManualPCCommunityRoomCreate(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_create.html'
# CommunityRoom ユーザーフォロー(PC)
class UserManualPCCommunityRoomHowToFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_howtofollow.html'
# CommunityRoom フォロー中ユーザー(PC)
class UserManualPCCommunityRoomFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follow.html'
# CommunityRoom フォローユーザーにDM(PC)
class UserManualPCCommunityRoomDMToFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dmtofollow.html'
# CommunityRoom フォローユーザー詳細移動(PC)
class UserManualPCCommunityRoomFollowGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follow_gotodetail.html'
# CommunityRoom フォローユーザー詳細画面(PC)
class UserManualPCCommunityRoomFollowDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follow_detail.html'
# CommunityRoom フォロー外す(PC)
class UserManualPCCommunityRoomFollowUnfollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follow_unfollow.html'
# CommunityRoom フォロワー(PC)
class UserManualPCCommunityRoomFollower(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follower.html'
# CommunityRoom フォロワーにDM(PC)
class UserManualPCCommunityRoomDMToFollower(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dmtofollower.html'
# CommunityRoom フォロワー詳細移動(PC)
class UserManualPCCommunityRoomFollowerGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follower_gotodetail.html'
# CommunityRoom フォロワー詳細画面(PC)
class UserManualPCCommunityRoomFollowerDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follower_detail.html'
# CommunityRoom フォロワーフォロー(PC)
class UserManualPCCommunityRoomFollowerFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_follower_follow.html'
# CommunityRoom DM受信リスト(PC)
class UserManualPCCommunityRoomDMSent(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_sent.html'
# CommunityRoom DM受信絞り込み機能(PC)
class UserManualPCCommunityRoomDMSentFiltering(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_sent_filtering.html'
# CommunityRoom DM受信詳細(PC)
class UserManualPCCommunityRoomDMSentDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_sent_detail.html'
# CommunityRoom DM受信通報(PC)
class UserManualPCCommunityRoomDMSentReport(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_sent_report.html'
# CommunityRoom DM送信リスト(PC)
class UserManualPCCommunityRoomDMSend(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_send.html'
# CommunityRoom DM送信絞り込み機能(PC)
class UserManualPCCommunityRoomDMSendFiltering(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_send_filtering.html'
# CommunityRoom DM送信詳細移動(PC)
class UserManualPCCommunityRoomDMSendGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_send_gotodetail.html'
# CommunityRoom DM送信詳細画面(PC)
class UserManualPCCommunityRoomDMSendDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_send_detail.html'
# CommunityRoom DM送信詳細削除(PC)
class UserManualPCCommunityRoomDMSendDetailDelete(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_dm_send_detail_delete.html'
# CommunityRoom 詳細画面(PC)
class UserManualPCCommunityRoomDetail(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_detail.html'
# CommunityRoom 詳細コメント追加(PC)
class UserManualPCCommunityRoomDetailAddComment(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_detail_comment.html'
# CommunityRoom 詳細コメント通報(PC)
class UserManualPCCommunityRoomDetailCommentReport(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_detail_comment_report.html'
# CommunityRoom 詳細コメントいいね!(PC)
class UserManualPCCommunityRoomDetailCommentGood(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_detail_comment_good.html'
# CommunityRoom 詳細コメントユーザーフォロー(PC)
class UserManualPCCommunityRoomDetailCommentFollow(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_detail_comment_follow.html'
# CommunityRoom いいね!(PC)
class UserManualPCCommunityRoomGood(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_good.html'
# CommunityRoom 通報(PC)
class UserManualPCCommunityRoomReport(generic.TemplateView):
    template_name = 'manual/user_manual_pc_communityroom_report.html'
# UserProfile(PC)
class UserManualPCUserProfile(generic.TemplateView):
    template_name = 'manual/user_manual_pc_userprofile.html'
# UserProfileプロフィール変更(PC)
class UserManualPCUserProfileChangeProfile(generic.TemplateView):
    template_name = 'manual/user_manual_pc_userprofile_changeprofile.html'
# DeleteAccount(PC)
class UserManualPCDeleteAccount(generic.TemplateView):
    template_name = 'manual/user_manual_pc_deleteaccount.html'
# LogOut(PC)
class UserManualPCLogOut(generic.TemplateView):
    template_name = 'manual/user_manual_pc_logout.html'

# タブレット
# トップページ(ログイン前,Tablet)
class UserManualTabletIndex(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_top_nav_before_login.html'
# お問い合わせ(ログイン前,Tablet)
class UserManualTabletContact(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_contact_before_login.html'
# メンタルチェック(ログイン前,Tablet)
class UserManualTabletMentalCheck(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mentalcheck_before_login.html'
# 専門家を探す(ログイン前,Tablet)
class UserManualTabletSearchLawyer(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_searchlawyer_before_login.html'
# サインアップ(Tablet)
class UserManualTabletSignUp(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_signup.html'
# ログイン(Tablet)
class UserManualTabletLogIn(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_login.html'
# トップページ(ログイン後,Tablet)
class UserManualTabletIndex2(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_top_nav_after_login.html'
# お問い合わせ(ログイン後,Tablet)
class UserManualTabletContact2(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_contact_after_login.html'
# メンタルチェック(ログイン後,Tablet)
class UserManualTabletMentalCheck2(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mentalcheck_after_login.html'
# 専門家を探す(ログイン後,Tablet)
class UserManualTabletSearchLawyer2(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_searchlawyer_after_login.html'
# MyPage(画面説明,Tablet)
class UserManualTabletMyPage(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage.html'
# MyPage 表示履歴(Tablet)
class UserManualTabletMyPageLog(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_log.html'
# MyPage 新規投稿(Tablet)
class UserManualTabletMyPageCreate(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_create.html'
# MyPage お気に入りリスト(Tablet)
class UserManualTabletMyPageFavorite(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_favorite.html'
# MyPage 詳細(Tablet)
class UserManualTabletMyPageDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_detail.html'
# MyPage 投稿更新(Tablet)
class UserManualTabletMyPageUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_detail_update.html'
# MyPage 投稿削除(Tablet)
class UserManualTabletMyPageDelete(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_delete.html'
# MyPage 返信作成(Tablet)
class UserManualTabletMyPageReply(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_detail_reply.html'
# MyPage いいね!(Tablet)
class UserManualTabletMyPageGood(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_comment_good.html'
# MyPage 通報(Tablet)
class UserManualTabletMyPageReport(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_report.html'
# MyPage フォロー(Tablet)
class UserManualTabletMyPageFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_mypage_follow.html'
# Everyone'sPost 画面説明(Tablet)
class UserManualTabletEveryonesPost(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost.html'
# Everyone'sPost いいね(Tablet)
class UserManualTabletEveryonesPostGood(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_good.html'
# Everyone'sPost 詳細(Tablet)
class UserManualTabletEveryonesPostDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail.html'
# Everyone'sPost 記事投稿者フォロー(Tablet)
class UserManualTabletEveryonesPostDetailFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_follow.html'
# Everyone'sPost 記事にコメント(Tablet)
class UserManualTabletEveryonesPostDetailComment(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_comment.html'
# Everyone'sPost 詳細いいね!(Tablet)
class UserManualTabletEveryonesPostDetailGood(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_good.html'
# Everyone'sPost 詳細お気に入り(Tablet)
class UserManualTabletEveryonesPostDetailFavorite(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_favorite.html'
# Everyone'sPost 詳細通報(Tablet)
class UserManualTabletEveryonesPostDetailReport(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_report.html'
# Everyone'sPost 詳細返信(Tablet)
class UserManualTabletEveryonesPostDetailReply(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_reply.html'
# Everyone'sPost 詳細コメントいいね!(Tablet)
class UserManualTabletEveryonesPostDetailCommentGood(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_comment_good.html'
# Everyone'sPost 詳細コメント通報(Tablet)
class UserManualTabletEveryonesPostDetailCommentReport(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_comment_report.html'
# Everyone'sPost 詳細コメントフォロー(Tablet)
class UserManualTabletEveryonesPostDetailCommentFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_everyonespost_detail_comment_follow.html'
# CommunityRoom(Tablet)
class UserManualTabletCommunityRoom(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom.html'
# CommunityRoom 再読み込み(Tablet)
class UserManualTabletCommunityRoomUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_update.html'
# CommunityRoom あなたの投稿(Tablet)
class UserManualTabletCommunityRoomYourPost(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_yourpost.html'
# CommunityRoom あなたの投稿更新(Tablet)
class UserManualTabletCommunityRoomYourPostUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_yourpost_update.html'
# CommunityRoom あなたの投稿削除(Tablet)
class UserManualTabletCommunityRoomYourPostDelete(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_yourpost_delete.html'
# CommunityRoom 新規投稿(Tablet)
class UserManualTabletCommunityRoomCreate(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_create.html'
# CommunityRoom ユーザーフォロー(Tablet)
class UserManualTabletCommunityRoomHowToFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_howtofollow.html'
# CommunityRoom フォロー中ユーザー(Tablet)
class UserManualTabletCommunityRoomFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follow.html'
# CommunityRoom フォローユーザーにDM(Tablet)
class UserManualTabletCommunityRoomDMToFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dmtofollow.html'
# CommunityRoom フォローユーザー詳細移動(Tablet)
class UserManualTabletCommunityRoomFollowGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follow_gotodetail.html'
# CommunityRoom フォローユーザー詳細画面(Tablet)
class UserManualTabletCommunityRoomFollowDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follow_detail.html'
# CommunityRoom フォロー外す(Tablet)
class UserManualTabletCommunityRoomFollowUnfollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follow_unfollow.html'
# CommunityRoom フォロワー(Tablet)
class UserManualTabletCommunityRoomFollower(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follower.html'
# CommunityRoom フォロワーにDM(Tablet)
class UserManualTabletCommunityRoomDMToFollower(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dmtofollower.html'
# CommunityRoom フォロワー詳細移動(Tablet)
class UserManualTabletCommunityRoomFollowerGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follower_gotodetail.html'
# CommunityRoom フォロワー詳細画面(Tablet)
class UserManualTabletCommunityRoomFollowerDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follower_detail.html'
# CommunityRoom フォロワーフォロー(Tablet)
class UserManualTabletCommunityRoomFollowerFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_follower_follow.html'
# CommunityRoom DM受信リスト(Tablet)
class UserManualTabletCommunityRoomDMSent(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_sent.html'
# CommunityRoom DM受信絞り込み機能(Tablet)
class UserManualTabletCommunityRoomDMSentFiltering(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_sent_filtering.html'
# CommunityRoom DM受信詳細(Tablet)
class UserManualTabletCommunityRoomDMSentDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_sent_detail.html'
# CommunityRoom DM受信通報(Tablet)
class UserManualTabletCommunityRoomDMSentReport(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_sent_report.html'
# CommunityRoom DM送信リスト(Tablet)
class UserManualTabletCommunityRoomDMSend(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_send.html'
# CommunityRoom DM送信絞り込み機能(Tablet)
class UserManualTabletCommunityRoomDMSendFiltering(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_send_filtering.html'
# CommunityRoom DM送信詳細移動(Tablet)
class UserManualTabletCommunityRoomDMSendGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_send_gotodetail.html'
# CommunityRoom DM送信詳細画面(Tablet)
class UserManualTabletCommunityRoomDMSendDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_send_detail.html'
# CommunityRoom DM送信詳細削除(Tablet)
class UserManualTabletCommunityRoomDMSendDetailDelete(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_dm_send_detail_delete.html'
# CommunityRoom 詳細画面(Tablet)
class UserManualTabletCommunityRoomDetail(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_detail.html'
# CommunityRoom 詳細コメント追加(Tablet)
class UserManualTabletCommunityRoomDetailAddComment(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_detail_comment.html'
# CommunityRoom 詳細コメント通報(Tablet)
class UserManualTabletCommunityRoomDetailCommentReport(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_detail_comment_report.html'
# CommunityRoom 詳細コメントいいね!(Tablet)
class UserManualTabletCommunityRoomDetailCommentGood(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_detail_comment_good.html'
# CommunityRoom 詳細コメントユーザーフォロー(Tablet)
class UserManualTabletCommunityRoomDetailCommentFollow(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_detail_comment_follow.html'
# CommunityRoom いいね!(Tablet)
class UserManualTabletCommunityRoomGood(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_good.html'
# CommunityRoom 通報(Tablet)
class UserManualTabletCommunityRoomReport(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_communityroom_report.html'
# UserProfile(Tablet)
class UserManualTabletUserProfile(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_userprofile.html'
# UserProfileプロフィール変更(Tablet)
class UserManualTabletUserProfileChangeProfile(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_userprofile_changeprofile.html'
# DeleteAccount(Tablet)
class UserManualTabletDeleteAccount(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_deleteaccount.html'
# LogOut(Tablet)
class UserManualTabletLogOut(generic.TemplateView):
    template_name = 'manual/user_manual_tablet_logout.html'

# スマートフォン
# トップページ(ログイン前,SP)
class UserManualSPIndex(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_top_nav_before_login.html'
# お問い合わせ(ログイン前,SP)
class UserManualSPContact(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_contact_before_login.html'
# メンタルチェック(ログイン前,SP)
class UserManualSPMentalCheck(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mentalcheck_before_login.html'
# 専門家を探す(ログイン前,SP)
class UserManualSPSearchLawyer(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_searchlawyer_before_login.html'
# サインアップ(SP)
class UserManualSPSignUp(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_signup.html'
# ログイン(SP)
class UserManualSPLogIn(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_login.html'
# トップページ(ログイン後,SP)
class UserManualSPIndex2(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_top_nav_after_login.html'
# お問い合わせ(ログイン後,SP)
class UserManualSPContact2(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_contact_after_login.html'
# メンタルチェック(ログイン後,SP)
class UserManualSPMentalCheck2(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mentalcheck_after_login.html'
# 専門家を探す(ログイン後,SP)
class UserManualSPSearchLawyer2(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_searchlawyer_after_login.html'
# MyPage(画面説明,SP)
class UserManualSPMyPage(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage.html'
# MyPage 表示履歴(SP)
class UserManualSPMyPageLog(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_log.html'
# MyPage 新規投稿(SP)
class UserManualSPMyPageCreate(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_create.html'
# MyPage お気に入りリスト(SP)
class UserManualSPMyPageFavorite(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_favorite.html'
# MyPage 詳細(SP)
class UserManualSPMyPageDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_detail.html'
# MyPage 投稿更新(SP)
class UserManualSPMyPageUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_detail_update.html'
# MyPage 投稿削除(SP)
class UserManualSPMyPageDelete(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_delete.html'
# MyPage 返信作成(SP)
class UserManualSPMyPageReply(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_detail_reply.html'
# MyPage いいね!(SP)
class UserManualSPMyPageGood(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_comment_good.html'
# MyPage 通報(SP)
class UserManualSPMyPageReport(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_report.html'
# MyPage フォロー(SP)
class UserManualSPMyPageFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_mypage_follow.html'
# Everyone'sPost 画面説明(SP)
class UserManualSPEveryonesPost(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost.html'
# Everyone'sPost いいね(SP)
class UserManualSPEveryonesPostGood(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_good.html'
# Everyone'sPost 詳細(SP)
class UserManualSPEveryonesPostDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail.html'
# Everyone'sPost 記事投稿者フォロー(SP)
class UserManualSPEveryonesPostDetailFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_follow.html'
# Everyone'sPost 記事にコメント(SP)
class UserManualSPEveryonesPostDetailComment(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_comment.html'
# Everyone'sPost 詳細いいね!(SP)
class UserManualSPEveryonesPostDetailGood(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_good.html'
# Everyone'sPost 詳細お気に入り(SP)
class UserManualSPEveryonesPostDetailFavorite(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_favorite.html'
# Everyone'sPost 詳細通報(SP)
class UserManualSPEveryonesPostDetailReport(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_report.html'
# Everyone'sPost 詳細返信(SP)
class UserManualSPEveryonesPostDetailReply(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_reply.html'
# Everyone'sPost 詳細コメントいいね!(SP)
class UserManualSPEveryonesPostDetailCommentGood(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_comment_good.html'
# Everyone'sPost 詳細コメント通報(SP)
class UserManualSPEveryonesPostDetailCommentReport(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_comment_report.html'
# Everyone'sPost 詳細コメントフォロー(SP)
class UserManualSPEveryonesPostDetailCommentFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_everyonespost_detail_comment_follow.html'
# CommunityRoom(SP)
class UserManualSPCommunityRoom(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom.html'
# CommunityRoom 再読み込み(SP)
class UserManualSPCommunityRoomUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_update.html'
# CommunityRoom あなたの投稿(SP)
class UserManualSPCommunityRoomYourPost(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_yourpost.html'
# CommunityRoom あなたの投稿更新(SP)
class UserManualSPCommunityRoomYourPostUpdate(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_yourpost_update.html'
# CommunityRoom あなたの投稿削除(SP)
class UserManualSPCommunityRoomYourPostDelete(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_yourpost_delete.html'
# CommunityRoom 新規投稿(SP)
class UserManualSPCommunityRoomCreate(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_create.html'
# CommunityRoom ユーザーフォロー(SP)
class UserManualSPCommunityRoomHowToFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_howtofollow.html'
# CommunityRoom フォロー中ユーザー(SP)
class UserManualSPCommunityRoomFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follow.html'
# CommunityRoom フォローユーザーにDM(SP)
class UserManualSPCommunityRoomDMToFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dmtofollow.html'
# CommunityRoom フォローユーザー詳細移動(SP)
class UserManualSPCommunityRoomFollowGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follow_gotodetail.html'
# CommunityRoom フォローユーザー詳細画面(SP)
class UserManualSPCommunityRoomFollowDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follow_detail.html'
# CommunityRoom フォロー外す(SP)
class UserManualSPCommunityRoomFollowUnfollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follow_unfollow.html'
# CommunityRoom フォロワー(SP)
class UserManualSPCommunityRoomFollower(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follower.html'
# CommunityRoom フォロワーにDM(SP)
class UserManualSPCommunityRoomDMToFollower(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dmtofollower.html'
# CommunityRoom フォロワー詳細移動(SP)
class UserManualSPCommunityRoomFollowerGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follower_gotodetail.html'
# CommunityRoom フォロワー詳細画面(SP)
class UserManualSPCommunityRoomFollowerDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follower_detail.html'
# CommunityRoom フォロワーフォロー(SP)
class UserManualSPCommunityRoomFollowerFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_follower_follow.html'
# CommunityRoom DM受信リスト(SP)
class UserManualSPCommunityRoomDMSent(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_sent.html'
# CommunityRoom DM受信絞り込み機能(SP)
class UserManualSPCommunityRoomDMSentFiltering(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_sent_filtering.html'
# CommunityRoom DM受信詳細(SP)
class UserManualSPCommunityRoomDMSentDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_sent_detail.html'
# CommunityRoom DM受信通報(SP)
class UserManualSPCommunityRoomDMSentReport(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_sent_report.html'
# CommunityRoom DM送信リスト(SP)
class UserManualSPCommunityRoomDMSend(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_send.html'
# CommunityRoom DM送信絞り込み機能(SP)
class UserManualSPCommunityRoomDMSendFiltering(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_send_filtering.html'
# CommunityRoom DM送信詳細移動(SP)
class UserManualSPCommunityRoomDMSendGoToDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_send_gotodetail.html'
# CommunityRoom DM送信詳細画面(SP)
class UserManualSPCommunityRoomDMSendDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_send_detail.html'
# CommunityRoom DM送信詳細削除(SP)
class UserManualSPCommunityRoomDMSendDetailDelete(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_dm_send_detail_delete.html'
# CommunityRoom 詳細画面(SP)
class UserManualSPCommunityRoomDetail(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_detail.html'
# CommunityRoom 詳細コメント追加(SP)
class UserManualSPCommunityRoomDetailAddComment(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_detail_comment.html'
# CommunityRoom 詳細コメント通報(SP)
class UserManualSPCommunityRoomDetailCommentReport(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_detail_comment_report.html'
# CommunityRoom 詳細コメントいいね!(SP)
class UserManualSPCommunityRoomDetailCommentGood(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_detail_comment_good.html'
# CommunityRoom 詳細コメントユーザーフォロー(SP)
class UserManualSPCommunityRoomDetailCommentFollow(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_detail_comment_follow.html'
# CommunityRoom いいね!(SP)
class UserManualSPCommunityRoomGood(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_good.html'
# CommunityRoom 通報(SP)
class UserManualSPCommunityRoomReport(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_communityroom_report.html'
# UserProfile(SP)
class UserManualSPUserProfile(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_userprofile.html'
# UserProfileプロフィール変更(SP)
class UserManualSPUserProfileChangeProfile(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_userprofile_changeprofile.html'
# DeleteAccount(SP)
class UserManualSPDeleteAccount(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_deleteaccount.html'
# LogOut(SP)
class UserManualSPLogOut(generic.TemplateView):
    template_name = 'manual/user_manual_smartphone_logout.html'


#利用規約
class TOSView(generic.TemplateView):
    template_name = 'terms_of_service.html'

#プライバシーポリシー
class PolicyView(generic.TemplateView):
    template_name = 'privacy_policy.html'