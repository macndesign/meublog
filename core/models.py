# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class PostQuerySet(models.query.QuerySet):
    def ativos(self):
        return self.filter(ativo=True)


class PostManager(models.Manager):
    def get_query_set(self):
        return PostQuerySet(self.model, using=self._db)

    def ativos(self):
        return self.get_query_set().ativos()


class Post(models.Model):
    autor = models.ForeignKey(
        to=User,
        help_text=_('Selecione o autor da postagem')
    )
    titulo = models.CharField(
        verbose_name=_(u'Título'),
        max_length=120,
        help_text=_(u'Digite um título adequado para a postagem')
    )
    sub_titulo = models.CharField(
        verbose_name=_(u'Sub-título'),
        max_length=120,
        help_text=_(u'Digite um sub-título adequado para a postagem')
    )
    data_publicacao = models.DateTimeField(
        verbose_name=_(u'Data de publicação'),
        auto_now_add=True,
        editable=True
    )
    conteudo = models.TextField(
        verbose_name=_(u'Conteúdo')
    )
    tags = TaggableManager()

    ativo = models.BooleanField(
        default=False
    )

    objects = PostManager()

    def get_absolute_url(self):
        return '/%s' % self.pk

    def __unicode__(self):
        return self.titulo
