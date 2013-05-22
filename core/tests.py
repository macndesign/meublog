# coding: utf-8
from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from datetime import datetime
import pytz


class BlogTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(username='admin', password='S3cr3t3', email="admin@admin.com")
        self.postagem = Post.objects.create(
            autor=self.usuario,
            titulo='Primeira postagem',
            sub_titulo=u'Subtítulo da primeira postagem',
            conteudo=u'Conteúdo de teste para o blog'
        )
        self.postagem_ativa = Post.objects.create(
            autor=self.usuario,
            titulo='Segunda postagem',
            sub_titulo=u'Subtítulo da primeira postagem',
            conteudo=u'Conteúdo de teste para o blog',
            ativo=True
        )
        self.postagem.tags.add('primeira', 'postagem', 'teste')
        self.postagem_ativa.tags.add('segunda', 'postagem')
        self.resp = self.client.get('/')

    def test_criacao_postagem(self):
        self.assertEqual(self.postagem.__unicode__(), 'Primeira postagem')
        self.assertEqual(self.postagem.get_absolute_url(), '/1')
        self.assertEqual(self.postagem.autor.username, 'admin')
        self.assertEqual(self.postagem.titulo, 'Primeira postagem')
        self.assertEqual(self.postagem.sub_titulo, u'Subtítulo da primeira postagem')

    def test_postagem_tem_data_publicacao(self):
        self.assertIsInstance(self.postagem.data_publicacao, datetime)
        self.assertEqual(self.postagem.data_publicacao.date(), datetime.now(tz=pytz.utc).date())
        self.assertEqual(self.postagem.data_publicacao.time().hour, datetime.now(tz=pytz.utc).time().hour)
        self.assertEqual(self.postagem.data_publicacao.time().minute, datetime.now(tz=pytz.utc).time().minute)

    def test_postagem_tem_tags(self):
        tags_postagem = [tag.name for tag in self.postagem.tags.all()]
        tags_postagem_ativa = [tag.name for tag in self.postagem_ativa.tags.all()]

        self.assertEqual(len(tags_postagem), 3)
        self.assertEqual(len(tags_postagem_ativa), 2)

        for tag in ['primeira', 'postagem', 'teste']:
            self.assertIn(tag, tags_postagem)

        for tag in ['segunda', 'postagem']:
            self.assertIn(tag, tags_postagem_ativa)

    def test_postagem_inativa_por_default(self):
        self.assertFalse(self.postagem.ativo)

    def test_pagina_inicial(self):
        self.assertEqual(self.resp.status_code, 200)
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    def test_postagem_na_pagina_inicial(self):
        self.assertContains(self.resp, 'Segunda postagem')
