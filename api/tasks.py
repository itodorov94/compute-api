from celery import shared_task
from .models import Result,Request
from .file import FileHandler
import logging
logger = logging.getLogger('server_log')

@shared_task()
def compute_request_content(req_id):

    result = 0
    request = Request.objects.get(id=req_id)
    result_model = Result.objects.create(request=request, result = result)
    logger.info('Result object created')
    file_handler = FileHandler(request.file_name.name)
    try:
        logger.info("Starting to calculate")
        result = file_handler.compute_file_content()
        result_model.result= result
        result_model.status=Result.DONE
        logger.info('File result calculated')
    except ValueError as err:
        logger.error(str(err))

        result_model.status = Result.ERROR

    result_model.save()
