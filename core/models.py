# coding: utf-8
from django.db import models
from taggit.managers import TaggableManager


class Post(models.Model):
    autor = models.ForeignKey(
        to='auth.User',
        help_text='Selecione o autor da postagem'
    )
    titulo = models.CharField(
        verbose_name=u'Título',
        max_length=120,
        help_text=u'Digite um título adequado para a postagem'
    )
    sub_titulo = models.CharField(
        verbose_name=u'Sub-título',
        max_length=120,
        help_text=u'Digite um sub-título adequado para a postagem'
    )
    data_publicacao = models.DateTimeField(
        verbose_name=u'Data de publicação',
        auto_now_add=True,
        editable=True
    )
    conteudo = models.TextField(
        verbose_name=u'Conteúdo'
    )
    tags = TaggableManager()

    def get_absolute_url(self):
        return '/%s' % self.pk

    def __unicode__(self):
        return self.titulo
