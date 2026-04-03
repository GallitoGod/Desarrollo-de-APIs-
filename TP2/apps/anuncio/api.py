from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer
from usuario.models import Usuario


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