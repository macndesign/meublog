from django.conf.urls import patterns, url
from core.views import PostListView, PostDetailView, PostCreateView, PostUpdateView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='listar'),
    url(r'^list/$', 'core.views.post_list', name='list'),

    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detalhar'),
    url(r'^detail/(?P<pk>\d+)/$', 'core.views.post_detail', name='detail'),

    url(r'^criar/$', PostCreateView.as_view(), name='criar'),
    url(r'^create/$', 'core.views.create', name='create'),

    url(r'^alterar/(?P<pk>\d+)/$', PostUpdateView.as_view(), name='alterar'),
    url(r'^update/(?P<pk>\d+)/', 'core.views.update', name='update'),
)