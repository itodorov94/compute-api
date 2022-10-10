"""
REST API views
"""

import logging
from rest_framework import generics, views, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .config import SUPPORTED_FORMATS
from .models import Request
from .tasks import compute_request_content

logger = logging.getLogger('server_log')


class RegisterView(generics.CreateAPIView):
    """
    View for registering new users
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class FileUploadView(views.APIView):
    """
    View for the file upload
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        username = request.user
        file_obj = request.FILES[list(request.FILES.keys())[0]]

        if not request.FILES:
            logger.error('Argument Filename not provided in the request')
            return Response('Please provide argument filename in request', status=status.HTTP_400_BAD_REQUEST)
        file_name = file_obj.name

        try:
            file_extension = file_name.rsplit('.')[1]
        except IndexError as e:
            logger.error(str(e))
            return Response('File name does not have an extension. Please provide one', status=status.HTTP_400_BAD_REQUEST)

        if file_extension in SUPPORTED_FORMATS:
            req = Request.objects.create(user_name=username, file_name=file_obj)
            logger.info('File is saved and request object created')
        else:
            logger.error(f'Received not supported file {file_extension}')
            return Response('File type not supported', status.HTTP_400_BAD_REQUEST)

        logger.info('Sending task to celery')
        compute_request_content.delay(req.id)

        return Response('Your file was uploaded and will be processed', status.HTTP_200_OK)
