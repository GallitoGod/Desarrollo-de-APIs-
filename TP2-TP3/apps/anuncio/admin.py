from django.contrib import admin
from .models import Anuncio, OfertaAnuncio

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'publicado_por',
        'precio_inicial',
        'activo',
        'fecha_inicio',
        'fecha_fin',
    )
    list_filter = ('activo', 'categorias', 'fecha_inicio')
    search_fields = ('titulo', 'descripcion', 'publicado_por__username')
    ordering = ('-fecha_inicio',)


@admin.register(OfertaAnuncio)
class OfertaAnuncioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'anuncio',
        'usuario',
        'precio_oferta',
        'es_ganador',
        'fecha_oferta',
    )
    list_filter = ('es_ganador', 'fecha_oferta')
    search_fields = ('anuncio__titulo', 'usuario__username')
    ordering = ('-precio_oferta',)