from django.contrib import admin
from django.urls import path, include
from .router import router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.anuncio.urls')), # Vistas manuales (APIViews)
    path('api/<str:version>/', include(router.urls)), # Router de los ViewSets
    # Tokens
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
