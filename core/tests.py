# coding: utf-8
from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from datetime import datetime
import pytz


class BlogTestCase(TestCase):
    def setUp(self):
        usuario = User.objects.create(username='admin', password='S3cr3t3', email="admin@admin.com")
        postagem = Post.objects.create(
            autor=usuario,
            titulo='Primeira postagem',
            sub_titulo=u'Subtítulo da primeira postagem',
            conteudo=u'Conteúdo de teste para o blog'
        )
        postagem.tags.add('primeira', 'postagem', 'teste')
        self.primeira_postagem = Post.objects.get(pk=1)

    def test_criacao_primeira_postagem(self):
        self.assertEqual(self.primeira_postagem.__unicode__(), 'Primeira postagem')
        self.assertEqual(self.primeira_postagem.get_absolute_url(), '/1')
        self.assertEqual(self.primeira_postagem.autor.username, 'admin')
        self.assertEqual(self.primeira_postagem.titulo, 'Primeira postagem')
        self.assertEqual(self.primeira_postagem.sub_titulo, u'Subtítulo da primeira postagem')

    def test_primeira_postagem_tem_data_publicacao(self):
        self.assertIsInstance(self.primeira_postagem.data_publicacao, datetime)
        self.assertEqual(self.primeira_postagem.data_publicacao.date(), datetime.now(tz=pytz.utc).date())
        self.assertEqual(self.primeira_postagem.data_publicacao.time().hour, datetime.now(tz=pytz.utc).time().hour)
        self.assertEqual(self.primeira_postagem.data_publicacao.time().minute, datetime.now(tz=pytz.utc).time().minute)

    def test_primeira_postagem_tem_tags(self):
        tags = [tag.name for tag in self.primeira_postagem.tags.all()]
        self.assertEqual(len(tags), 3)
        for tag in ['primeira', 'postagem', 'teste']:
            self.assertIn(tag, tags)

    def test_primeira_postagem_inativa_por_default(self):
        self.assertFalse(self.primeira_postagem.ativo)
