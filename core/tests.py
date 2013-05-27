# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc
from .models import Post
from datetime import datetime


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
        self.assertEqual(self.postagem.data_publicacao.date(), datetime.now(tz=utc).date())
        self.assertEqual(self.postagem.data_publicacao.time().hour, datetime.now(tz=utc).time().hour)
        self.assertEqual(self.postagem.data_publicacao.time().minute, datetime.now(tz=utc).time().minute)

    def test_postagem_tem_tags(self):
        tags_postagem = [tag.name for tag in self.postagem.tags.all()]
        tags_postagem_ativa = [tag.name for tag in self.postagem_ativa.tags.all()]

        # Testando se a 1ª postagem tem 3 tags e a segunda tem 2 tags
        self.assertEqual(len(tags_postagem), 3)
        self.assertEqual(len(tags_postagem_ativa), 2)

        # Testando especificamente se as tags estão ou não nas postagens
        for tag in ['primeira', 'postagem', 'teste']:
            self.assertIn(tag, tags_postagem)

        self.assertNotIn('segunda', tags_postagem)

        for tag in ['segunda', 'postagem']:
            self.assertIn(tag, tags_postagem_ativa)

        for tag in ['primeira', 'teste']:
            self.assertNotIn(tag, tags_postagem_ativa)

    # Testando se a postagem é criada por padrão como inativa
    def test_postagem_inativa_por_default(self):
        self.assertFalse(self.postagem.ativo)

    # Testando se a página inicial está disponível e com o template correto
    def test_pagina_inicial(self):
        self.assertEqual(self.resp.status_code, 200)
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    # Testando se aparece apenas a postagem que está ativa na página inicial
    def test_postagem_na_pagina_inicial(self):
        self.assertContains(self.resp, 'Segunda postagem')
        self.assertNotContains(self.resp, 'Primeira postagem')
