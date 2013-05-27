from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('autor', 'titulo', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao', 'ativo')
    search_fields = ['autor', 'titulo']

admin.site.register(Post, PostAdmin)
