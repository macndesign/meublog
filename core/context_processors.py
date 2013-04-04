# coding: utf-8
from taggit.models import Tag
from core.models import Post


def active_post_tags(request):
    # Lista tags referentes aos posts ativos
    posts = Post.objects.ativos()
    active_tags = [post.tags.all() for post in posts]

    tag_full_list = [t for tag in active_tags for t in tag]
    all_tags = Tag.objects.all()
    tags = [tag for tag in all_tags if tag_full_list.count(tag)]

    return {'tags': tags, 'tag_full_list': tag_full_list}
