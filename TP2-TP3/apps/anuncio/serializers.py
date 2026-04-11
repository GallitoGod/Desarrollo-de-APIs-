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
    categorias = CategoriaSerializer(many = True)
    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora'
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']

    def create(self, validated_data):
        categorias_data = validated_data.pop('categorias', [])
        anuncio = Anuncio.objects.create(**validated_data)
        # aca tengo que usar '**' porque viene de un JSON transformado a diccionario de python por el serializador
        for categoria_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                # no necesito usar created ya que me diria True si crea esa categoria y False en caso contrario
                nombre = categoria_data.get('nombre'),
                defaults = categoria_data
            )
            anuncio.categorias.add(categoria)
            # mientras que aca no porque categoria es un objeto vivo por el ORM cuando uso 'get_or_create'.
            # no necesita cambios, esta en el estado correcto para agregarlo a la BD.
        return anuncio