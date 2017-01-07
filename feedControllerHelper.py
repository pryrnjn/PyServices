from feedSource import Twitter, Instagram


def get_feed(term="narendra modi", sort="timestamp", count=20):
    feed = get_twitter_feed(term) + get_instagram_feed(term)
    feed.sort(key=lambda a: a.created_at, reverse=True)
    return feed[0:20]


def get_twitter_feed(term="narendra modi"):
    return Twitter(term).get_content()


def get_instagram_feed(term="narendra modi"):
    return Instagram(term).get_content()
