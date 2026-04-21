from django_filters import rest_framework as filters
from apps.anuncio.models import Categoria, Anuncio

class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'activa']

class AnuncioFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    
    precio_min = filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    precio_max = filters.NumberFilter(field_name='precio_inicial', lookup_expr='lte')
    
    desde_fecha = filters.DateTimeFilter(field_name='fecha_inicio', lookup_expr='gte')

    class Meta:
        model = Anuncio
        fields = ['titulo', 'categorias', 'precio_min', 'precio_max', 'desde_fecha']