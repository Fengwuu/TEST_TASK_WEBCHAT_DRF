from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

"""
This is swagger. 
The library necessary for working with the API allows you to explore the finished API.
API testing was also carried out using Postman
"""

schema_view = get_schema_view(
    openapi.Info(
        title="Filipp test task webchat",
        default_version='v1',
        description="This is my webchat",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="filipp.pustovoitenko.work@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<str:format>.json.yaml', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
