# -*- coding:utf-8 -*-
from wsgiref.simple_server import make_server


class WebApplication:
    headers = []
    status = '200 OK'

    def __init__(self):
        pass

    def __call__(self, env, start_response):
        self.status = '200 OK'
        del self.headers[:]
        result = self._invoke(env)
        start_response(self.status, self.headers)
        if isinstance(result, str):
            return iter([bytes(result, 'utf8')])
        return iter(result)

    def _invoke(self, env):
        path = env['PATH_INFO']
        return self.send_file(path[1:])

    def not_found(self):
        self.status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found\n"

    def send_file(self, path):
        try:
            if path.endswith('html'):
                self.header('Content-type', 'text/html; charset=UTF-8')
            with open(path, mode='r', encoding='UTF-8') as file:
                return file.read()
        except:
            return self.not_found()

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
