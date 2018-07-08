import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
sys.path.append('/var/www/vhodove.bg/system/root')
sys.path.append('/home/taiwo/Desktop/WORKING_FOLDER/freelancer/dzago/root/root/')
from django.core.wsgi import get_wsgi_application


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'vhodove.settings'
    application = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    #http_server.listen(8001)
    http_server.listen(8001, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

