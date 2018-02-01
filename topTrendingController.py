import csv
import traceback
from urlparse import parse_qs
import re
from utils import *

date_matcher = re.compile(r'\d{4}-\d{2}-\d{2}')
loaded_data = []
score_data = dict()


def load_data():
    file_path = "data/instagram/instagram.csv"

    with open(file_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for row in reader:
            loaded_data.append(row)
    loaded_data.sort(key=lambda x: (date_matcher.match(x[2]).group(), int(x[3])), reverse=True)


def update_score(url, score):
    if url not in score_data:
        score_data[url] = 0
    score_data[url] += score


load_data()


class TopTrendingController:
    def __init__(self, server):
        self.server = server
    def __del__(self):
        pass

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

    def do_PUT(self, path_obj=None):
        query_arr = parse_qs(path_obj.query) or {}
        url = int(query_arr.get("url", [None])[0])
        score = int(query_arr.get("score", [0])[0])
