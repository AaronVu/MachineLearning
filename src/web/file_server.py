# -*- coding:utf-8 -*-
import inspect
from wsgiref.simple_server import make_server


class Controller:
    NAME = "Controller"
    TYPE = "WebApp Controller"
    SUCCESS = 1
    FAILE = 0


class WebApplication:

    headers = []

    def __init__(self, urls=(), fvars={}):
        self._urls = dict(url for url in urls)
        self._fvars = fvars

    def __call__(self, env, start_response):
        print(env)
        self._status = '200 OK'
        del self.headers[:]
        result = self._invoke(env)
        start_response(self._status, self.headers)
        return iter(result)

    def _invoke(self, env):
        path = env['PATH_INFO']
        print(path)
        args = env['QUERY_STRING']
        if self._urls.get(path):
            func_name = self._urls[path]
            clazz_name = path.split('/')[1].capitalize() + Controller.NAME
            clazz = self._fvars.get(clazz_name)
            if hasattr(clazz, func_name) and hasattr(clazz, "TYPE") and getattr(clazz, "TYPE") == Controller.TYPE:
                func = getattr(clazz, func_name)
                args = self.args_handler(args, func)
                return func(clazz(), **args)
        return self.not_found()

    def not_found(self):
        self._status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found\n"

    @staticmethod
    def send_file(path):
        with open(path, 'r') as file:
            return file.read()

    @staticmethod
    def args_handler(args, func):
        parmas = {}
        func_args = inspect.getargspec(func).args
        if args:
            ps = args.split("&")
            for p in ps:
                parma = p.split("=")
                if parma and len(parma) > 1:
                    if parma[0] in func_args:
                        parmas[parma[0]] = parma[1]
        return parmas

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))


def main():
    web_app = WebApplication()
    httpd = make_server('127.0.0.1', 8088, web_app)
    tips = httpd.socket.getsockname()
    print('http://{0}:{1}/index.html'.format(*tips))
    httpd.serve_forever()


if __name__ == "__main__":
    main()