from django.contrib import admin
from core.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('autor', 'titulo', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao')
    search_fields = ['autor', 'titulo']

admin.site.register(Post, PostAdmin)
