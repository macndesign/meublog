# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Post


class TestPostList(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(
            username='admin',
            password='S3cr3t3',
            email="admin@admin.com"
        )

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

        self.resp = self.client.get(reverse('post:listar'))

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
