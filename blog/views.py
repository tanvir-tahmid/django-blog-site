from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Post
from .forms import CommentForm

# Create your views here.

class IndexPageView(ListView):
  template_name = "blog/index.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "posts"

  def get_queryset(self):
      queryset = super().get_queryset()
      data = queryset[:3]
      return data

class AllPostsView(ListView):
  template_name = "blog/all-posts.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "all_posts"


class SinglePostView(DetailView):
  def is_stored_post(self, request, post_id):
    unread = request.session.get("unread")
    if unread is not None:
      is_saved_for_later = post_id in unread
    else:
      is_saved_for_later = False

    return is_saved_for_later

  def get(self, request, slug):
    post = Post.objects.get(slug=slug)
  
    context = {
      "post": post,
      "post_tags": post.tags.all(),
      "comment_form": CommentForm(),
      "comments": post.comments.all().order_by("-id"),
      "saved_for_later": self.is_stored_post(request, post.id)
    }
    return render(request, "blog/post-detail.html", context)

  def post(self, request, slug):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(slug=slug)

    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.post = post
      comment.save()
      return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

    context = {
    "post": post,
    "post_tags": post.tags.all(),
    "comment_form": CommentForm(),
    "comments": post.comments.all().order_by("-id"),
    "saved_for_later": self.is_stored_post(request, post.id)
    }

    return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):
    def get(self, request):
        unread = request.session.get("unread")

        context = {}

        if unread is None or len(unread) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
          posts = Post.objects.filter(id__in=unread)
          context["posts"] = posts
          context["has_posts"] = True

        return render(request, "blog/unread.html", context)


    def post(self, request):
        unread = request.session.get("unread")

        if unread is None:
          unread = []

        post_id = int(request.POST["post_id"])

        if post_id not in unread:
          unread.append(post_id)
        else:
          unread.remove(post_id)

        request.session["unread"] = unread
        
        return HttpResponseRedirect("/unread")