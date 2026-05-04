from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer, CategoriaV2Serializer
from apps.usuario.models import Usuario
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoriaFilter, AnuncioFilter
from .pagination import StandardResultsSetPagination

class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer




#     --------        ViewSets     -------------

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'activa']
    pagination_class = StandardResultsSetPagination

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


    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)


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
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)