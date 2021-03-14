from drf_yasg import openapi
from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.utils import force_real_str, is_list_view
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings

from commons.global_constants import DETAIL
from swagger.constants import GENERIC_ERROR, VALIDATION_ERROR


class ErrorResponseAutoSchema(SwaggerAutoSchema):
    def get_generic_error_schema(self):
        return openapi.Schema(
            'Generic Error',
            type=openapi.TYPE_OBJECT,
            properties={
                DETAIL: openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            },
            required=[DETAIL]
        )

    def get_validation_error_schema(self):
        return openapi.Schema(
            'Validation Error',
            type=openapi.TYPE_OBJECT,
            properties={
                api_settings.NON_FIELD_ERRORS_KEY: openapi.Schema(
                    description='List of validation errors causing bad request',
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
            },
        )

    def get_response_serializers(self):
        responses = super().get_response_serializers()
        definitions = self.components.with_scope(openapi.SCHEMA_DEFINITIONS)
        definitions.setdefault(GENERIC_ERROR, self.get_generic_error_schema)
        definitions.setdefault(VALIDATION_ERROR, self.get_validation_error_schema)

        if self.get_request_serializer():
            responses.setdefault(exceptions.ValidationError.status_code, openapi.Response(
                description=force_real_str(exceptions.ValidationError.default_detail),
                schema=openapi.SchemaRef(definitions, VALIDATION_ERROR)
            ))

        security = self.get_security()
        if (not security or len(security) > 0) and AllowAny not in self.view.permission_classes:
            responses.setdefault(status.HTTP_401_UNAUTHORIZED, openapi.Response(
                description="Authentication credentials were not provided.",
                schema=openapi.SchemaRef(definitions, GENERIC_ERROR)
            ))
            responses.setdefault(exceptions.PermissionDenied.status_code, openapi.Response(
                description="Permission denied.",
                schema=openapi.SchemaRef(definitions, GENERIC_ERROR)
            ))

        if not is_list_view(self.path, self.method, self.view) or '{' in self.path:
            responses.setdefault(exceptions.NotFound.status_code, openapi.Response(
                description="Not found.",
                schema=openapi.SchemaRef(definitions, GENERIC_ERROR)
            ))

        return responses
