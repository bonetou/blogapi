from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context.get("view", None)
        logger.error("Unhandled exception in view %s: %s", view, exc, exc_info=True)

        return Response(
            {"detail": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
