import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .forms import InquiryForm, DiaryCreateForm, MessageCreateForm, CommentCreateForm
from .models import Avengers, Message, Comment

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

class AccuseListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'object_list2'
    model = Avengers
    template_name = 'accuse_list.html'
    paginate_by = 40

    def get_queryset(self):
        accuses = Avengers.objects.all().order_by('-created_at')[:199]
        return accuses

class AccuseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Avengers
    template_name = 'accuse_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['com_list'] = self.object.comment_set.filter(parent__isnull=True)
        return context

class MessageView(generic.ListView):
    context_object_name = 'comment_list'
    model = Message
    template_name = 'community_room.html'
    paginate_by = 100

    def get_queryset(self):
        messages = Message.objects.all().order_by('-created_at')[:1000]
        return messages

class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Message
    template_name = 'message_detail.html'

class MessageCreateView(generic.CreateView):
    model = Message
    template_name = 'message_create.html'
    form_class = MessageCreateForm
    success_url = reverse_lazy('avengers:comment_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, 'メッセージを投稿しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "メッセージ投稿に失敗しました。")
        return super().form_invalid(form)

class PersonalMessageView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'p_message_list'
    model = Message
    template_name = 'your_comment.html'
    paginate_by = 100

    def get_queryset(self):
        diaries = Message.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    template_name = 'message_update.html'
    form_class = MessageCreateForm

    def get_success_url(self):
        return reverse_lazy('avengers:comment_list')

    def form_valid(self, form):
        messages.success(self.request, '投稿内容を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "投稿内容の更新に失敗しました。")
        return super().form_invalid(form)

class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('avengers:comment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "投稿内容を削除しました。")
        return super().delete(request, *args, **kwargs)

def comment_create(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Avengers, pk=post_pk)
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('avengers:accuse_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post
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
        reply.save()
        return redirect('avengers:accuse_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'comment_form.html', context)