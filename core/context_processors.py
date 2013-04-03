# coding: utf-8
from taggit.models import Tag


def view_in_all_pages(request):
    tags = Tag.objects.all()
    return {'tags': tags}
