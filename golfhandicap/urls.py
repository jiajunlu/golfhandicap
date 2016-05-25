from django.conf.urls import url
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    url(r'^$', views.index, name='golfhandicap'),
    url(r'^allplayers$', views.allplayers, name='allplayers'),
    url(r'^games$', views.games, name='games'),
    url(r'^rules$', TemplateView.as_view(template_name='golfhandicap/rules.html')),
]
