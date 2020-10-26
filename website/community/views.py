from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserAskingForm, CommentForm
from .models import UserAsking, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic import (ListView, CreateView, DetailView, DeleteView,
                                  UpdateView, View)
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from accounts.models import UserProfile
from notifications.models import Notification
from website import settings


@method_decorator(login_required, name='dispatch')
# Create question by user
class UserAskingView(CreateView, SingleObjectMixin):
    queryset = UserAsking.objects.all()
    template_name = 'community/asking_question.html'
    form_class = UserAskingForm
    model = UserAsking
    slug_field = 'ask_slug'
    slug_url_kwarg = 'user_slug'

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            asking = form.save(commit=False)
            asking.title = form.cleaned_data['title']
            asking.question = form.cleaned_data['question']
            asking.field = form.cleaned_data['field']
            UserAsking.objects.create(userprofile_id=self.request.user.userprofile.id,
                                      title=asking.title,
                                      question=asking.question,
                                      field=asking.field)
            request.session.get('delete_post', False)
            return redirect('community:user_questions')


# List all questions + search
class UserQuestions(ListView):
    template_name = 'community/user_questions.html'
    context_object_name = 'all_objects'
    queryset = UserAsking

    def get_context_data(self, object_list=queryset, **kwargs):
        context = super().get_context_data(**kwargs)
        # paginator
        context['all_objects'] = UserAsking.objects.all()
        paginator = Paginator(context['all_objects'], 5)
        page_number = self.request.GET.get('page_number')
        context['all_objects'] = paginator.get_page(page_number)
        # search
        context['query'] = self.request.GET.get("query", '')
        if context['query']:
            all_objects = UserAsking.objects.all().order_by('-date')
            context['all_objects'] = all_objects.filter(
                Q(title__contains=self.request.GET['query']) |
                Q(question__contains=self.request.GET['query']) |
                Q(field__contains=self.request.GET['query'])
            )
        return context

from django.core import serializers
# Detail question and Create comment
class QuestionDetail(DetailView, SingleObjectMixin):
    template_name = 'community/question_view.html'
    slug_field = 'ask_slug'
    slug_url_kwarg = 'user_slug'
    model = UserAsking
    queryset = UserAsking.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_question'] = UserAsking.objects.get(clone_title=self.object)
        self_post = UserAsking.objects.get(clone_title=self.object)
        post_slug = UserAsking.objects.get(ask_slug=self_post.ask_slug)
        context['summation'] = post_slug.likes.count() - post_slug.dislikes.count()
        context['comment_form'] = CommentForm or None
        comments_count = Comment.objects.filter(userasking=UserAsking.objects.get(clone_title=self.object))
        context['comments_count'] = comments_count.count()
        context['is_liked'] = False
        context['is_dislike'] = False
        context['comment_like'] = False
        # context to like the post
        if LikePost.as_view():
            if post_slug.dislikes.filter(username=self.request.user).exists():
                context['is_liked'] = False
            elif post_slug.likes.filter(username=self.request.user).exists():
                context['is_liked'] = True
            else:
                context['is_liked'] = False
        # context to dis-like the post
        if DisLikePost.as_view():
            if post_slug.likes.filter(username=self.request.user).exists():
                context['is_dislike'] = False
            elif post_slug.dislikes.filter(username=self.request.user).exists():
                context['is_dislike'] = True
            else:
                context['is_dislike'] = False
        context['comment_like'] = False
        # context to like the comment
        # context yo add favorite
        context['favorite'] = False
        if AddFavorite.as_view():
            if post_slug.favorite.filter(username=self.request.user).exists():
                context['favorite'] = True
            else:
                context['favorite'] = False
        return context

    def post(self, request, user_slug, *args, **kwargs):
        my_question = UserAsking.objects.get(ask_slug=user_slug)
        userprof = UserProfile.objects.get(userasking__ask_slug=user_slug)
        comment_form = CommentForm(request.POST, instance=request.user)
        name = "%s %s" % (self.request.user.first_name, self.request.user.last_name)
        username = self.request.user.username
        logo = self.request.user.userprofile.logo.url
        if comment_form.is_valid():
            comment_request = self.request.POST.get('comment', None)
            comment_form = Comment.objects.create(comment=comment_request,
                                                  userasking_id=my_question.id,
                                                  userprofile_id=userprof.id,
                                                  name=name,
                                                  username=username,
                                                  logo=logo,
                                                  comment_slug=my_question.ask_slug
                                                  )
            request.session['switch_comment'] = True
            request.session['comment_id'] = comment_form.id

            return redirect('community:question_view', user_slug)
            # return redirect('community:question_view', comment_form.userasking.ask_slug)
        return render(request, 'community/question_view.html', {'comment_form': comment_form})


@method_decorator(login_required, name='dispatch')
# Delete post
class DeletePost(DeleteView, SingleObjectMixin):
    model = UserAsking
    slug_field = 'ask_slug'
    slug_url_kwarg = 'user_slug'
    template_name = 'community/question_view.html'
    queryset = UserAsking.objects.all()
    success_url = reverse_lazy('community:user_questions')

    def get_object(self, queryset=None):
        self.request.session['delete_post'] = True
        slug = self.request.POST['delete_form']
        settings.DELETE_POST = True
        q = UserAsking.objects.get(ask_slug=slug).id
        self.request.session['notify_delete'] = q
        return self.get_queryset().filter(ask_slug=slug).get()


@method_decorator(login_required, name='dispatch')
# Update Post
class UpdatePost(UpdateView, SingleObjectMixin):
    slug_field = 'ask_slug'
    slug_url_kwarg = 'user_slug'
    queryset = UserAsking.objects.all()
    form_class = UserAskingForm
    template_name = 'community/update_question.html'
    success_url = '/community/'

    # def get_success_url(self):
    #     self.object = self.get_object()
    #     title = UserAsking.objects.get(title=self.object)
    #     slug = UserAsking.objects.get(title=title).ask_slug
    #     print(self.queryset.get_absolute_url())
        #return redirect(reverse('community:question_view', kwargs={'user_slug': self.object.ask_slug}))
        #return redirect(reverse_lazy('community:question_view', kwargs={'user_slug': slug}))


@method_decorator(login_required, name='dispatch')
# Delete comment
class DeleteComment(View, SingleObjectMixin):
    model = Comment
    pk_url_kwarg = 'pk'
    template_name = 'community/question_view.html'
    queryset = Comment.objects.all()

    def post(self, request, *args, pk, **kwargs):
        c_slug = Comment.objects.get(pk=pk)
        u_slug = UserAsking.objects.get(comment=c_slug)
        c_slug.delete()
        return redirect(reverse('community:question_view', kwargs={'user_slug': u_slug.ask_slug}))


@method_decorator(login_required, name='dispatch')
# Edit comment
class UpdateComment(UpdateView, SingleObjectMixin):
    slug_field = 'comment_slug'
    slug_url_kwarg = 'user_slug'
    form_class = CommentForm
    queryset = Comment.objects.all()
    template_name = 'community/update_comment.html'

    def get_success_url(self):
        c_slug = Comment.objects.get(comment=self.request.POST['comment'])
        u_slug = UserAsking.objects.get(comment=c_slug)
        return reverse('community:question_view', kwargs={'user_slug': u_slug.ask_slug})


@method_decorator(login_required, name='dispatch')
# Like post function
class LikePost(View, SingleObjectMixin):
    template_name = 'community/question_view.html'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(UserAsking, ask_slug=request.POST.get('post_slug'))
        if post.dislikes.filter(username=request.user).exists(): # like is False
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
        elif post.likes.filter(username=request.user).exists(): # like is True
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect(post.get_absolute_url())


@method_decorator(login_required, name='dispatch')
# Dislike post function
class DisLikePost(View, SingleObjectMixin):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(UserAsking, ask_slug=request.POST.get('post_dislike_slug'))
        if post.likes.filter(username=request.user).exists():
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
        elif post.dislikes.filter(username=request.user).exists():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
        return redirect(post.get_absolute_url())


@method_decorator(login_required, name='dispatch')
# Like comment function
class LikeComment(View, SingleObjectMixin):

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=request.POST.get('like-comment'))
        if comment.likes.filter(username=request.user).exists():
            comment.likes.remove(request.user)
            comment.notify_comment.remove(request.user)
        else:
            comment.likes.add(request.user)
            comment.notify_comment.add(request.user)
        return redirect(comment.get_absolute_url())


@method_decorator(login_required, name='dispatch')
# Add favourite
class AddFavorite(View, SingleObjectMixin):
    def post(self, request, user_slug):
        post = get_object_or_404(UserAsking, ask_slug=request.POST.get('save-fav'))
        if post.favorite.filter(username=request.user).exists():
            messages.success(self.request, 'unsaved', extra_tags='unsaved')
            post.favorite.remove(request.user)
        else:
            messages.success(self.request, 'saved', extra_tags='saved')
            post.favorite.add(request.user)
        return redirect(post.get_absolute_url())


class Inboxes(ListView):
    template_name = 'community/inboxes.html'
    queryset = Notification.objects.all()
    context_object_name = 'notifies'