import csv
import os
import re
import threading
import traceback
from urlparse import parse_qs

from utils import *

date_matcher = re.compile(r'\d{4}-\d{2}-\d{2}')
file_path = "data/instagram/instagram.csv"
last_modified_date = {'d': 0}
loaded_data = []
header = None
score_data = dict()


def load_data():
    last_modified_date['d'] = os.path.getmtime(file_path)
    del loaded_data[:]
    with open(file_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        header = reader.next()
        for row in reader:
            loaded_data.append(row)
    loaded_data.sort(key=lambda x: (date_matcher.match(x[2]).group(), int(x[3])), reverse=True)


def refresh_data():
    if os.path.getmtime(file_path) > last_modified_date['d']:
        load_data()
    threading.Timer(137, refresh_data).start()


def update_score(url, score):
    if url not in score_data:
        score_data[url] = 0
    score_data[url] += score


def execute_update(final=False):
    if len(score_data):
        with open(file_path, 'rb') as csv_file:
            writer = csv.writer(csv_file)
            for row in loaded_data:
                score = score_data.get(row[1], 0)
                row[3] += score
                if row[3] > -10:
                    writer.writerow(row)
        last_modified_date['d'] = os.path.getmtime(file_path)
        loaded_data.sort(key=lambda x: (date_matcher.match(x[2]).group(), int(x[3])), reverse=True)
    if not final:
        threading.Timer(120, execute_update).start()


def cleanup():
    execute_update(final=True)


refresh_data()
execute_update()


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

    def do_PUT(self, path_obj=None):
        query_arr = parse_qs(path_obj.query) or {}
        url = query_arr.get("url", [None])[0]
        score = int(query_arr.get("score", [0])[0])
        if url and score != 0:
            update_score(url, score)
