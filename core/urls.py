from django.conf.urls import patterns, url
from core.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name='listar'),
                       url(r'^list/$', 'core.views.post_list', name='list'),

                       # posts relacionados a uma tag
                       url(r'^posts-tagged-related/(?P<pk>\d+)/$', 'core.views.post_list_tagged_related',
                           name='posts-tagged-related'),

                       url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detalhar'),
                       url(r'^detail/(?P<pk>\d+)/$', 'core.views.post_detail', name='detail'),

                       url(r'^criar/$', PostCreateView.as_view(), name='criar'),
                       url(r'^create/$', 'core.views.create', name='create'),

                       url(r'^alterar/(?P<pk>\d+)/$', PostUpdateView.as_view(), name='alterar'),
                       url(r'^update/(?P<pk>\d+)/', 'core.views.update', name='update'),

                       url(r'^excluir/(?P<pk>\d+)/$', PostDeleteView.as_view(), name='excluir'),
                       url(r'^delete/(?P<pk>\d+)/$', 'core.views.delete', name='delete'))
