from rest_framework import serializers
from .models import Categoria, Anuncio

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'activa',
        ]


class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), 
        many=True
    )

    class Meta:
        model = Anuncio
        fields = [
            'id', 'titulo', 'descripcion', 'precio_inicial', 
            'imagen', 'fecha_inicio', 'fecha_fin', 'activo', 
            'categorias', 'publicado_por', 'oferta_ganadora'
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']