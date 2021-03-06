import sys
import traceback
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse

import os

dir = os.path.dirname(__file__)

PORT_NUMBER = 8080
import pusher

global pusher_client
pusher_client = pusher.Pusher(
    app_id='287804',
    key='772c22382c098e14619e',
    secret='dc7d5f4df95fb0061fbd',
    ssl=True
)
active_channels = set()

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
            try:
                self.wfile.write(open(os.path.join(dir, "web-content", "index.html"), 'rb').read())
            except:
                traceback.print_exc()
                self.wfile.write("Something Wrong!")
        return


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
        print 'KeyboardInterrupt, shutting down the web server'
        server.socket.close()
