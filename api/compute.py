
# from .config import OPERATIONS_DICT, RESOURCES
# from .models import Result,Request


# class CSVComputer:

#     def compute(self, req_pk):
#         request = Request.objects.get(pk=req_pk)
#         result = Result.objects.create(request=request, result=0)
#         operation_result = 0
#         with open(RESOURCES / request.file_name, 'r') as f:
#             operations = [line.strip() for line in f.readlines()]

#         for operation_str in operations:
#             self._validate(operation_str)
#             parts = operation_str.split(',')
#             operator = parts[1]
#             operation = OPERATIONS_DICT[operator]
#             operation_result += operation(float(parts[0]), float(parts[2])) # Check input
#         result.status = Result.DONE
#         result.result = operation_result
#         result.save()

#     def _validate(self, operation):
#         parts = operation.split(',')
#         if len(parts) != 3:
#             print('File has invalid entry')
#             raise ValueError

