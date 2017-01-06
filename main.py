from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
import sys

PORT_NUMBER = 8080


class MainController(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        path_obj = urlparse(self.path)
        if path_obj.path.find("/feed") == 0:
            from feedController import FeedController
            FeedController(self).do_GET(path_obj)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Hello World!")
        return


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        PORT_NUMBER = int(args[0]) if len(args) else PORT_NUMBER
        # Creating the web server and asigning the handler
        server = HTTPServer(('', PORT_NUMBER), MainController)
        print('Started httpserver on port ', PORT_NUMBER)

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print 'KeyboardInterrupt, shutting down the web server'
        server.socket.close()
