from django.contrib import admin
from django.urls import path, include
from .router import router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


schema_view = get_schema_view(
   openapi.Info(
      title="API de Subastas",
      default_version='v1',
      description="Documentación oficial del sistema de anuncios y ofertas.",
      contact=openapi.Contact(email="contacto@subastas.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.anuncio.urls')), # Vistas manuales (APIViews)
    path('api/<str:version>/', include(router.urls)), # Router de los ViewSets
    # Tokens
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
