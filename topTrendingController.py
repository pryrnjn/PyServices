import csv
import traceback
from urlparse import parse_qs

from utils import *

print "importing"

loaded_data = []


def load_data():
    file_path = "data/instagram/instagram.csv"

    with open(file_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for row in reader:
            loaded_data.append(row)
    loaded_data.sort(key=lambda x: x[2], reverse=True)


load_data()


class TopTrendingController:
    def __init__(self, server):
        self.server = server

    def do_GET(self, path_obj=None):
        query_arr = parse_qs(path_obj.query) or {}
        offset = int(query_arr.get("offset", [0])[0])
        limit = int(query_arr.get("limit", [20])[0])
        response = {}
        try:
            feed = loaded_data[offset:offset + limit]
            response["feed"] = feed
            if len(feed) == limit:
                response["next"] = "/trending?offset=%d&limit=%d" % (offset + len(feed), limit)
            response = build_json_response(response)
        except:
            self.server.send_error(500, "We couldn't serve you! We're working on this..")
            traceback.print_exc()  # log errors!!!
            return
        self.server.send_response(200)
        self.server.send_header('Content-type', 'application/json')
        self.server.end_headers()
        self.server.wfile.write(response)
