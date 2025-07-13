from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/', include('blog.urls')),
    path("v1/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('v1/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
