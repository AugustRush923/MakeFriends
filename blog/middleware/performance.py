import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('performance')


def performance_middleware(get_response):
    def middleware(request):
        start_time = time.time()

        response = get_response(request)

        duration = time.time() - start_time

        response['X-Page-Duration-ms'] = int(duration * 1000)
        logger.info(
            f'{duration}  {request.META["REQUEST_METHOD"]}  {request.path}  {request.GET.dict()}  '
            f'{request.META["REMOTE_ADDR"]}')
        return response

    return middleware


class PerformanceMiddleware(MiddlewareMixin):
    """"""
    def __init__(self, get_response):
        super(PerformanceMiddleware, self).__init__(get_response)

    def process_request(self, request):
        print(request.path_info)
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        response['Duration-ms'] = int(duration * 1000)
        logger.info(
            f'{duration}  {request.META["REQUEST_METHOD"]}  {request.path}  {request.GET.dict()}  '
            f'{request.META["REMOTE_ADDR"]}')
        return response
