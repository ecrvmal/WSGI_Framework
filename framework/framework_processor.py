# from app.views import *
from sys import path

from vmal_framework.app.views import PageNotFound404

path.append('../')
from app.views import *
from framework.request_processing import RequestProcessing


class Framework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        # print(f'environ = {environ}')
        route = environ['PATH_INFO']

        if not route.endswith('/'):
            route = f'{route}/'

        if route in self.routes:
            view = self.routes[route]
        else:
            view = PageNotFound404()

        # ------------------- Front Controller ---------------------#

        request = {}
        for front in self.fronts:
            front(request)
        RequestProcessing.get_method(environ, request)
        print(f'method : {request["method"]}       ', end='')
        if request['method'] == 'GET':
            RequestProcessing.process_get_request(environ, request)
            print(f' request_data : {request["data"]}')
        if request['method'] == 'POST':
            RequestProcessing.process_post_request(environ, request)
            print(f'request_params: {request["request_params"]}')


        # ------------------- end of Front Controller ---------------------#

        # --------------------   Page Controller --------------------------#

        code, body = view(request)
        # --------------------   End of Page Controller --------------------------#

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode()]