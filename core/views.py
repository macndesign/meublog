# coding: utf-8
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from taggit.models import Tag
from .models import Post
from .forms import PostForm


# FBV - Function Based-Views

def post_list(request):
    posts = Post.objects.ativos()

    # Mostra 25 posts por página
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a página 1.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Se a página está fora da faixa (e.g. 9999), mostra a ultima página.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'core/post_list.html', {'page_obj': page_obj})


def post_list_tagged_related(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list_tagged_related = Post.objects.ativos().filter(tags__slug__in=[tag.slug])
    return render(request, 'core/post_list_tagged_related.html', {'post_list_tagged_related': post_list_tagged_related,
                                                                  'tag_name': tag.name})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/post_detail.html', {'object': post})


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            s = form.save()
            messages.success(request, u'Postagem criada com sucesso.')
            return redirect(s.get_absolute_url())

        messages.error(request, u'O formulário está inválido.')

    else:
        form = PostForm()
    return render(request, 'core/post_form.html', {'form': form, 'CREATE': True})


def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            s = form.save()
            messages.success(request, u'Postagem alterada com sucesso.')
            return redirect(s.get_absolute_url())

        messages.error(request, u'O formulário está inválido.')

    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_form.html', {'form': form, 'CREATE': False})


def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, u'Postagem excluída com sucesso.')
        return redirect(reverse_lazy('post:list'))

    return render(request, 'core/post_confirm_delete.html', {'object': post})


# CBV - Class Based-Views


class PostListView(ListView):
    model = Post
    paginate_by = 3
    queryset = Post.objects.ativos()


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['CREATE'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, u'Postagem criada com sucesso.')
        return super(PostCreateView, self).get_success_url()

    def form_invalid(self, form):
        messages.error(self.request, u'O formulário está inválido.')
        return super(PostCreateView, self).form_invalid(form)


class PostUpdateView(UpdateView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['CREATE'] = False
        return context

    def get_success_url(self):
        messages.success(self.request, u'Postagem alterada com sucesso.')
        return super(PostUpdateView, self).get_success_url()

    def form_invalid(self, form):
        messages.error(self.request, u'O formulário está inválido.')
        return super(PostUpdateView, self).form_invalid(form)


class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(self.request, u'Postagem excluída com sucesso.')
        return reverse_lazy('post:listar')
