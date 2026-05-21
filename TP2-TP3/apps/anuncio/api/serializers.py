from rest_framework import serializers
from apps.anuncio.models import Anuncio, Categoria
from django.utils import timezone
from .utils import cotizar_usd

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['uuid', 'nombre', 'activa',]
        read_only_fields = ['uuid']

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre de la categoría es muy corto")
        return value
    
    def validate(self, data):
        if 'principal' in data['nombre'].lower() and not data['activa']:
            raise serializers.ValidationError("No se puede desactivar la Categoria principal")
        return data




class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True)
    precio_usd = serializers.SerializerMethodField()

    class Meta:
        model = Anuncio
        fields = ['uuid', 'titulo', 'descripcion', 'precio_inicial', 'precio_usd', 'fecha_inicio', 'fecha_fin', 'activo', 'categorias', 'publicado_por']
        read_only_fields = ['publicado_por', 'uuid', 'precio_usd']




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
        return data
    
    def get_precio_usd(self, obj):
        
        tasa = cotizar_usd()
        
        if tasa and obj.precio_inicial:
            precio_usd = float(obj.precio_inicial) * tasa
            return round(precio_usd, 2)
        return "No disponible temporalmente"

class CategoriaV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
        ]