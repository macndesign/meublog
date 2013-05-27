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
            conteudo=u'Primeiro conteúdo para o blog'
        )

        self.postagem.tags.add('primeira', 'postagem', 'teste')

        self.postagem_ativa = Post.objects.create(
            autor=self.usuario,
            titulo='Segunda postagem',
            sub_titulo=u'Subtítulo da primeira postagem',
            conteudo=u'Segundo conteúdo para o blog',
            ativo=True
        )

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
        """
        Testando se a 1ª postagem tem 3 tags e a segunda tem 2 tags
        e especificamente se as tags estão ou não nas postagens
        """

        tags_postagem = [tag.name for tag in self.postagem.tags.all()]
        tags_postagem_ativa = [tag.name for tag in self.postagem_ativa.tags.all()]

        self.assertEqual(len(tags_postagem), 3)
        self.assertEqual(len(tags_postagem_ativa), 2)

        for tag in ['primeira', 'postagem', 'teste']:
            self.assertIn(tag, tags_postagem)

        self.assertNotIn('segunda', tags_postagem)

        for tag in ['segunda', 'postagem']:
            self.assertIn(tag, tags_postagem_ativa)

        for tag in ['primeira', 'teste']:
            self.assertNotIn(tag, tags_postagem_ativa)

    def test_postagem_inativa_por_default(self):
        """
        Testando se a postagem é criada por padrão como inativa
        """
        self.assertFalse(self.postagem.ativo)

    def test_pagina_inicial(self):
        """
        Testando se a página inicial está disponível e com o template correto
        """
        self.assertEqual(self.resp.status_code, 200)
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    def test_postagem_na_pagina_inicial(self):
        """
        Testando se aparece apenas a postagem que está ativa na página inicial
        """
        self.assertContains(self.resp, 'Segunda postagem')
        self.assertNotContains(self.resp, 'Primeira postagem')

    def test_tags_corretas_na_pagina_inicial(self):
        """
        Testando se tem apenas as tags da postagem ativa na página
        """
        self.assertContains(self.resp, 'segunda')
        self.assertContains(self.resp, 'postagem')
        self.assertNotContains(self.resp, 'primeira')
        self.assertNotContains(self.resp, 'teste')
