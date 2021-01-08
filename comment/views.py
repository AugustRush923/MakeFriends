from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from blog.models import Post
from .forms import CommentForm


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=int(post_id))
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.target = post

            comment.save()

            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
