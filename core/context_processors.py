# coding: utf-8
from core.models import Post


def view_in_all_pages(request):
    # Lista tags referentes aos posts ativos
    posts = Post.objects.ativos()
    active_tags = [post.tags.all() for post in posts]
    tags = list({t for tag in active_tags for t in tag})
    return {'tags': tags}
