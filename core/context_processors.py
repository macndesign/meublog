# coding: utf-8
from core.models import Post


def view_in_all_pages(request):
    # Lista tags referentes aos posts ativos
    posts = Post.objects.ativos()
    tags = [post.tags.all() for post in posts]

    join_tags = []
    for tag in tags:
        for t in tag:
            join_tags.append(t)

    tags = list(set(join_tags))

    return {'tags': tags}
