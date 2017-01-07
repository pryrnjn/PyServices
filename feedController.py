import json
import traceback
from urlparse import parse_qs

from feedControllerHelper import *

print "importing"


def build_json_response(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)


class FeedController:
    def __init__(self, server):
        self.server = server

    def do_GET(self, path_obj=None):
        global feed
        query_arr = parse_qs(path_obj.query).get("q", None)
        if query_arr is None or len(query_arr) == 0 or query_arr[0].strip() == "":
            self.server.send_error(400, "Provide a valid query!")
        else:
            try:
                if path_obj.path.find("/feed/twitter") == 0:
                    feed = get_twitter_feed(query_arr[0])
                elif path_obj.path.find("/feed/insta") == 0:
                    feed = get_instagram_feed(query_arr[0])
                elif path_obj.path == "/feed":
                    feed = get_feed(query_arr[0])
                else:
                    self.server.send_error(400, "Provide a valid query!")
                response = build_json_response(feed)
            except:
                self.server.send_error(500, "We couldn't serve you! We're working on this..")
                traceback.print_exc()  # log errors!!!
                return
            self.server.send_response(200)
            self.server.send_header('Content-type', 'application/json')
            self.server.end_headers()
            self.server.wfile.write(response)
