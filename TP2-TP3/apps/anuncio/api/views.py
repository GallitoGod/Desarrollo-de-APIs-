from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from apps.anuncio.models import Categoria, Anuncio, OfertaAnuncio
from .serializers import CategoriaSerializer, AnuncioSerializer, CategoriaV2Serializer
from apps.usuario.models import Usuario
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from apps.anuncio.filters import CategoriaFilter, AnuncioFilter
from apps.anuncio.pagination import StandardResultsSetPagination
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from decimal import Decimal



#     --------        ViewSets     -------------

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'activa']
    pagination_class = StandardResultsSetPagination
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return CategoriaV2Serializer 
        return CategoriaSerializer


class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnuncioFilter
    ordering_fields = ['titulo']
    pagination_class = StandardResultsSetPagination
    lookup_field = 'uuid'


    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.publicado_por != self.request.user:
            raise PermissionDenied("No tienes permiso para modificar este anuncio.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.publicado_por != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este anuncio.")
        instance.delete()


    @action(detail=True, methods=['get'])
    def tiempo_restante(self, request, pk=None):
        anuncio = self.get_object()

        if not anuncio.fecha_fin:
            return Response({"mensaje": "Este anuncio no tiene una fecha de finalización definida."}, status=200)

        ahora = timezone.now()
        tiempo_restante = anuncio.fecha_fin - ahora

        if tiempo_restante.total_seconds() <= 0:
            return Response({
                "estado": "Finalizado",
                "tiempo_restante": "0 días, 0 horas, 0 minutos"
            })

        dias = tiempo_restante.days
        segundos = tiempo_restante.seconds
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60

        return Response({
            "estado": "Activo",
            "tiempo_restante_texto": f"{dias} días, {horas} horas, {minutos} minutos",
            "detalle": {
                "dias": dias,
                "horas": horas,
                "minutos": minutos
            }
        })
    
    @action(detail=True, methods=['post'])
    def ofertar(self, request, pk=None, **kwargs):
        anuncio = self.get_object()
        precio_enviado = request.data.get('precio_oferta')
        precio_decimal = Decimal(str(precio_enviado))

        if anuncio.publicado_por == request.user:
            return Response({"error": "No se puede realizar ofertas a tu propio anuncio."}, status=status.HTTP_403_FORBIDDEN)

        if not anuncio.activo:
            return Response({"error": "Anuncio no activo."}, status=status.HTTP_400_BAD_REQUEST)
        
        if anuncio.fecha_fin < timezone.now():
            return Response({"error": "El tiempo de la subasta ha finalizado."}, status=status.HTTP_400_BAD_REQUEST)

        
        
        if not precio_enviado:
            return Response(
                {"error": "Debes incluir el campo 'precio_oferta' en tu petición."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            nueva_oferta = OfertaAnuncio(
                anuncio=anuncio,
                usuario=request.user,
                precio_oferta=precio_decimal
            )
            
            nueva_oferta.clean() 
            nueva_oferta.save()

            return Response({
                "mensaje": "Oferta registrada exitosamente.",
                "oferta_id": nueva_oferta.id,
                "precio_ofertado": nueva_oferta.precio_oferta
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)





# ------------ APIVIEW --------------------





class CategoriaListaAPIView(APIView):
    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetalleAPIView(APIView):
    def get(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AnuncioListaAPIView(APIView):
    def get(self, request, format=None):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnuncioSerializer(data=request.data)
        if serializer.is_valid():
            usuario_por_defecto = Usuario.objects.first()
            
            if not usuario_por_defecto:
                return Response(
                    {"error": "No hay ningún usuario en la base de datos para asignar al anuncio."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(publicado_por=usuario_por_defecto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AnuncioDetalleAPIView(APIView):

    def get(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        
  
        if anuncio.publicado_por != request.user:
            raise PermissionDenied("No tienes permiso para modificar este anuncio.")
            
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        
        if anuncio.publicado_por != request.user:
            raise PermissionDenied("No tienes permiso para eliminar este anuncio.")
            
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer