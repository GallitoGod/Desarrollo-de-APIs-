from rest_framework import serializers
from .models import Categoria, Anuncio
from django.utils import timezone

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'activa',
        ]




class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True)

    class Meta:
        model = Anuncio
        fields = [
            'id', 'titulo', 'descripcion', 'precio_inicial', 
            'imagen', 'fecha_inicio', 'fecha_fin', 'activo', 
            'categorias', 'publicado_por', 'oferta_ganadora'
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']

    def validate_fecha_inicio(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La fecha de inicio no puede ser en el pasado")
        return value
    
    def validate_precio_inicial(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un valor positivo")
        return value
    
    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise serializers.ValidationError({"fecha_fin": "La fecha de finalización debe ser posterior a la fecha de inicio"})