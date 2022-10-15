from atexit import register
from django.urls import path, register_converter
from . import views, converters

register_converter(converters.EUNEorEUWConverter, 'serv')

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('<serv:server>/<str:nickname>/', views.account, name='account'),
    path('<serv:server>/<str:nickname>/f0rmp4tht0h4ndl3upd4t3/', views.update, name='update'),
    path('f0rmp4tht0h4ndl3r3d1r3ct/', views.rdr, name='rdr'),
    path('f0rmp4tht0h4ndl3l4ngu4g3/', views.language, name='language'),
]