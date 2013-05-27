# coding: utf-8
# coding: utf-8
from django.test import TestCase
from ..forms import PostForm


class TestPostForm(TestCase):
    def test_has_fields(self):
        """
        Form must have 4 fields.
        """
        form = PostForm()
        fields = ['autor', 'titulo', 'sub_titulo', 'conteudo', 'tags', 'ativo']
        self.assertItemsEqual(fields, form.fields)
        self.assertNotIn('data_publicacao', form.fields)
