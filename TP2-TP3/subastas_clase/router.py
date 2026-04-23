from rest_framework import routers
from apps.anuncio.api import CategoriaViewSet, AnuncioViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(prefix='categoria', viewset=CategoriaViewSet)
router.register(prefix='anuncio', viewset=AnuncioViewSet)
urlpatterns = router.urls

