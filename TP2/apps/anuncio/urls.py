from django.urls import path
from .api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView, CategoriaListaGenericView, CategoriaDetalleGenericView

app_name = 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('anuncios/', AnuncioListaAPIView.as_view(), name='anuncio-lista'),
    path('anuncios/<int:pk>/', AnuncioDetalleAPIView.as_view(), name='anuncio-detalle'),
    path('generic-view/categoria', CategoriaListaGenericView.as_view()),
    path('generic-view/categoria/<int:pk>', CategoriaDetalleGenericView.as_view()),
]