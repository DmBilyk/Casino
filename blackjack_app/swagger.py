from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path
from rest_framework import permissions

# Create a schema view for the API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Blackjack API",  # Title of the API
        default_version='v1',  # Default version of the API
        description="API for Blackjack game",  # Description of the API
        terms_of_service="https://www.example.com/terms/",  # Terms of service URL
        contact=openapi.Contact(email="contact@example.com"),  # Contact email
        license=openapi.License(name="BSD License"),  # License information
    ),
    public=True,  # Make the schema public
    permission_classes=(permissions.AllowAny,),  # Allow any permissions
)

# Define URL patterns for the schema views
urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # JSON schema view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI view
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI view
]