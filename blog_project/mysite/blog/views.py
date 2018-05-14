from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                 DetailView, CreateView,
                                 UpdateView, DeleteView)

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    # django will look for post_list.html by default
    # connected model
    model = Post

    def get_queryset(self):
        # Get all objects from the Post model and filter it based on the given query
        # field lookup : __lte(lookuptype) = 'less than or equal to'
        # Wqual SQL query : SELECT * FROM Post where published_date <= timezone.now();
        # filer first and then order them
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    # django will look for post_detail.html by default
    model = Post

# mixins are for class based views, decorators work for function based views
class CreatePostView(LoginRequiredMixin, CreateView):
    # incase the user is not logged in, where should go
    login_url = '/login/'
    # redirect to detail view on successful login
    redirect_filed_name = 'blog/post_detail.html'
    # connected form
    form_class = PostForm
    model = Post

# login required for updating views as well
class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_filed_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    # here all fields are editable(no include or exclude specified)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # where should to go after deleting a post
    # reverse_lazy wil wait till the post gets deleted
    # post_list - name of the url pattern to match
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_filed_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

##################################################
##################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish
    return redirect('posts_detail', pk=pk)

# login_required decorator is for function based views
# This view required to be logged in
@login_required
def add_comment_to_post(request, pk):
    # pk - primary which actually link comment to the post
    # get post object or return 404 page
    post = get_object_or_404(Post, pk=pk)
    # someone filled in the form and press
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # is_vaild - all fields are filled
        if form.is_valid():
            comment = form.save(commit=False)
            # connecting foreign key post - for the comment
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # saving it in the extra variable since it will be deleted but needed for redirect
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
