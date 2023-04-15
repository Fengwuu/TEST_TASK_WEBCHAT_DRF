from django.urls import path, include, register_converter
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Define a custom validator function to validate the user id field


def validate_user_id(value):
    # Check if a user with the given id exists
    if not User.objects.filter(id=value).exists():
        raise ValidationError(
            _("Invalid user id")
        )

# Define a custom URL converter for positive integers


class PositiveIntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


# Register the custom URL converter
register_converter(PositiveIntConverter, 'pos_int')


urlpatterns = [
    #  list and create threads
    path('api/v1/threads/',
         ThreadsViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='list'),

    # messages for a specific thread
    path('api/v1/threads/<pos_int:pk>/messages/',
         ThreadsViewSet.as_view({'get': 'get_messages'}), name='get_messages'),

    # details for a specific thread
    path('api/v1/threads/<pos_int:pk>/',
         ThreadDetailView.as_view(), name='thread_detail'),

    # new message endpoint
    path('api/v1/message/',
         MessageViewSet.as_view({'post': 'create'}), name='message'),

    # list threads for a specific user
    path('api/v1/threads/by_user/<pos_int:user_id>/',
         ThreadListByUserAPIView.as_view(), name='thread_list_by_user',
         kwargs={'validators': [validate_user_id]}),

    # obtain JWT  token
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # refresh JWT  token
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
