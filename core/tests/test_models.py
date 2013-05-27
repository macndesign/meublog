# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc
from core.models import Post
from datetime import datetime


class TestPostModel(TestCase):
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

    def test_postagem_tem_data_publicacao(self):
        self.assertIsInstance(self.postagem.data_publicacao, datetime)
        self.assertEqual(
            self.postagem.data_publicacao.strftime('%Y-%m-%d %H:%M'),
            datetime.now(tz=utc).strftime('%Y-%m-%d %H:%M')
        )

    def test_criacao_postagem(self):
        self.assertEqual(self.postagem.__unicode__(), 'Primeira postagem')
        self.assertEqual(self.postagem.get_absolute_url(), '/1')
        self.assertEqual(self.postagem.autor.username, 'admin')
        self.assertEqual(self.postagem.titulo, 'Primeira postagem')
        self.assertEqual(self.postagem.sub_titulo, u'Subtítulo da primeira postagem')

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

    def test_manager_postagens_ativas(self):
        postagens_ativas = Post.objects.ativos()
        self.assertEqual(len(postagens_ativas), 1)
        self.assertNotEqual(postagens_ativas[0].titulo, 'Primeira postagem')
        self.assertEqual(postagens_ativas[0].titulo, 'Segunda postagem')
