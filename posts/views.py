from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse_lazy('list')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse_lazy('list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('list')

class DraftListView(ListView):
    model = Post
    template_name = 'posts/drafts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='draft')
