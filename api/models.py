from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

class Request(ExportModelOperationsMixin('request'),models.Model):

    user_name = models.CharField(max_length=32, blank=True, null=True)
    file_name = models.FileField(upload_to='resources/', default='')
    upload_date = models.DateTimeField(auto_now_add=True)


class Result(ExportModelOperationsMixin('result'),models.Model):

    DONE = 'Done'
    ERROR = 'Error'
    IN_PROGRESS = 'In progress'
    STATUSES = (
        (DONE, 'DONE'),
        (ERROR, 'ERROR'),
        (IN_PROGRESS, 'In Progress'),
            )

    result = models.DecimalField(decimal_places=2, max_digits=100, blank=True)
    result_date = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUSES, default=IN_PROGRESS)
