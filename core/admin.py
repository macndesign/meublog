from django.contrib import admin
from core.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['autor', 'titulo', 'data_publicacao']
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(Post, PostAdmin)
