import os
import sys
import traceback
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse

import topTrendingController

this_dir = os.path.dirname(__file__)

PORT_NUMBER = 8080


class MainController(BaseHTTPRequestHandler):
    # Handler for the GET requests

    def do_GET(self):
        path_obj = urlparse(self.path)
        if path_obj.path.find("/trending/update") == 0:
            from topTrendingController import TopTrendingController
            TopTrendingController(self).do_PUT(path_obj)
        elif path_obj.path.find("/trending") == 0:
            from topTrendingController import TopTrendingController
            TopTrendingController(self).do_GET(path_obj)
        elif path_obj.path.find("/status") == 0:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                self.wfile.write(open(os.path.join(this_dir, "data", "instagram", "scrapper_status.txt"), 'r').read())
            except:
                traceback.print_exc()
                self.wfile.write("Something Wrong!")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                self.wfile.write(open(os.path.join(this_dir, "web-content", "index.html"), 'rb').read())
            except:
                traceback.print_exc()
                self.wfile.write("Something Wrong!")
        return


def cleanup():
    print 'cleanup!!'
    topTrendingController.execute_update(True)


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        PORT_NUMBER = int(args[0]) if len(args) else PORT_NUMBER
        # Creating the web server and asigning the handler
        server = HTTPServer(('0.0.0.0', PORT_NUMBER), MainController)
        print('Started httpserver on port ', PORT_NUMBER)

        # Wait forever for incoming http requests
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
    finally:
        cleanup()
