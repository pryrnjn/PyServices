import csv
import os
import random
import re
import subprocess
import threading
import time
import traceback
from urlparse import parse_qs

from utils import *

date_matcher = re.compile(r'\d{4}-\d{2}-\d{2}')
file_path = "data/instagram/instagram.csv"
scrapper_proj = "../scrapper/"
scraped_data_file = scrapper_proj + "data/instagram/instagram.csv"
last_modified_data = {'d': 0, 'header': [], 'scraped_date': 0, 'len': 0}
loaded_data = []
removed_data = []
header = None
score_data = dict()
visitors = list()


def load_data():
    last_modified_data['d'] = os.path.getmtime(file_path)
    del loaded_data[:]
    with open(file_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        last_modified_data['header'] = reader.next()
        for row in reader:
            if int(row[3]) > 0:
                loaded_data.append(row)
            else:
                removed_data.append(row)
    # loaded_data.sort(key=lambda x: (date_matcher.match(x[2]).group(), int(x[3])), reverse=True)
    last_modified_data['len'] = len(loaded_data)
    write_status("refreshed in memory data from file")


def refresh_data():
    if os.path.getmtime(scraped_data_file) > last_modified_data['scraped_date']:
        update_data_csv()
    if os.path.getmtime(file_path) > last_modified_data['d']:
        load_data()
    threading.Timer(1800, refresh_data).start()


def update_score(url, score):
    if url not in score_data:
        score_data[url] = 0
    score_data[url] += score


def execute_update(final=False):
    if len(visitors):
        with open("data/instagram/visitors.csv", 'a') as csv_file:
            writer = csv.writer(csv_file)
            for visitor in visitors:
                writer.writerow(visitor)
            del visitors[:]
    if len(score_data):
        write_status("writing updated score to file")
        with open(file_path, 'wb') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(last_modified_data['header'])
            for row in loaded_data:
                score = score_data.pop(row[1], 0)
                row[3] = int(row[3]) + score
                writer.writerow(row)

            for row in removed_data:
                score = score_data.pop(row[1], 0)
                row[3] = int(row[3]) + score
                writer.writerow(row)

        last_modified_data['d'] = os.path.getmtime(file_path)
        loaded_data.sort(key=lambda x: (date_matcher.match(x[2]).group(), int(x[3])), reverse=True)
    if not final:
        threading.Timer(120, execute_update).start()


def update_data_csv():
    write_status("updating data from scrapped data")
    url_set = set()
    last_modified_data['scraped_date'] = os.path.getmtime(scraped_data_file)
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for row in reader:
            url_set.add(row[1])
    with open(scraped_data_file, 'r') as input_file, open(file_path, 'a') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        reader.next()
        for row in reader:
            if row[1] not in url_set:
                writer.writerow(row)
                url_set.add(row[1])


def run_scrapper():
    try:
        write_status("attempting start scrapper")
        if time.time() - os.path.getmtime(scraped_data_file) > 3600:
            status = subprocess.check_call([scrapper_proj + "bin/run_scrapy.sh", "instagram", "instagram.csv", "csv",
                                            scrapper_proj + "bin/scrapy.properties"])
        else:
            write_status("recently run, skipping!")
        update_data_csv()
        write_status("updated data csv from scrapped content")
        threading.Timer(14400, run_scrapper).start()
    except subprocess.CalledProcessError as e:
        status = e.returncode
        threading.Timer(3600, run_scrapper).start()
    finally:
        write_status("completed scrapper with status %d" % status)


def write_status(msg):
    with open("data/instagram/scrapper_status.txt", 'a') as status_file:
        status_file.write(
            "[%s IST] - %s\n" % (time.strftime("%Y-%h-%d %H:%M:%S", time.gmtime(time.time() + 19800)), str(msg)))


def cleanup():
    execute_update(final=True)


refresh_data()
execute_update()


# threading.Timer(0, run_scrapper).start() # handled by crontab


class TopTrendingController:
    def __init__(self, server):
        self.server = server

    def do_GET(self, path_obj=None):
        visitors.append([self.server.headers.get('Host'),
                         self.server.client_address[0],
                         time.strftime("%Y-%h-%d-%H-%M", time.gmtime(time.time() + 19800))])
        query_arr = parse_qs(path_obj.query) or {}
        offset = int(query_arr.get("offset", [0])[0])
        limit = int(query_arr.get("limit", [20])[0])
        sort_by = query_arr.get("sort", ["date"])[0]
        response = {}
        try:
            feed = loaded_data[offset:offset + limit]
            indices = random.sample(xrange(last_modified_data['len']), 5)
            response["feed"] = [loaded_data[i] for i in indices]
            # if len(feed) == limit:
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
        response = {'updated': False}
        if url and score != 0:
            update_score(url, score)
            response['updated'] = True
        response = build_json_response(response)
        self.server.send_response(200)
        self.server.send_header('Content-type', 'application/json')
        self.server.end_headers()
        self.server.wfile.write(response)
