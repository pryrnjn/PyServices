import json
import time

import thread

from feedSource import Twitter, Instagram

from main import pusher_client, active_channels

REFRESH_INTERVAL = 30


def get_feed(term="narendra modi"):
    twitter_feed = Twitter(term)
    insta_feed = Instagram(term)

    content = consolidate_feed([twitter_feed, insta_feed])

    sent_ids = set([(c.id, c.source) for c in content])
    register_for_push_content([twitter_feed, insta_feed], term, "feed", sent_ids)
    return content


def consolidate_feed(feeds, max_count=20):
    max_count = max(max_count, 20)
    contents = []
    for feed in feeds:
        contents += feed.get_content()
    contents.sort(key=lambda a: a.created_at, reverse=True)

    return contents[0:max_count]


def register_for_push_content(feeds, pusher_channel, pusher_event, ids):
    thread.start_new_thread(push_content, (feeds, pusher_channel, pusher_event, ids))
    pass


def push_content(feeds, pusher_channel="", pusher_event="", sent_ids=set()):
    pusher_channel = ".".join(pusher_channel.split())

    if pusher_channel in active_channels:
        print "Thread already exist for channel: '%s', quitting this!" % pusher_channel
        return

    active_channels.add(pusher_channel)
    if pusher_channel and pusher_event and feeds:
        while 1:
            time.sleep(REFRESH_INTERVAL)
            if pusher_client.channel_info(pusher_channel)["occupied"]:  # more than 1 subscription
                contents = []
                for content in consolidate_feed(feeds):
                    if (content.id, content.source) not in sent_ids:
                        sent_ids.add((content.id, content.source))
                        contents.append(content)
                print "sending to channel %s" % pusher_channel
                pusher_client.trigger(pusher_channel, pusher_event, build_json_response(contents))
            else:
                print "thread closing for channel %s " % pusher_channel
                break
    active_channels.remove(pusher_channel)

def build_json_response(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)
