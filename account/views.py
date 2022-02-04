from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login


from .forms import RegisterForm, CommentForm

from .forms import EmailPostForm
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, 'post.html', {'posts': posts})


def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post,
                                                    'form': form})


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'review.html',
                 {'post': post,
                  'comments': comments,
                  'comment_form': comment_form})




