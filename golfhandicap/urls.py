from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='golfhandicap'),
    url(r'^allplayers$', views.allplayers, name='allplayers'),
]
