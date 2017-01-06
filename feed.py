import twitter, json
from instagram.client import InstagramAPI

twitter_api = twitter.Api(consumer_key='wZDNRfzFbdOs59J6D6H7rEhmW',
                          consumer_secret='PwAPmfI18yff8dt6ta1YRncgDH1hHmsUEo1oUyKiedlMJkCaH7',
                          access_token_key='124545778-HLphpuUHHgmei9o9pUXX0BAN1T4PT8QG7jvYYaYW',
                          access_token_secret='tUilFXaRYb5uQYlv9OXSGT97ZtVijkxyjBoW07kxXxYmY')
instagram_api = InstagramAPI(access_token="838346436.7334de0.9c346c16a42a4adeb4346a0b21149572",
                             client_secret="8438f728ca2944d086c119aca1fbce34")


class Source:
    TWITTER, INSTAGRAM = "twitter", "instagram"


class Feed:
    def __init__(self):
        pass


class Content:
    def __init__(self, text, img, link, owner, created_at, source):
        self.text = text
        self.img = img
        self.link = link
        self.owner = owner
        self.created_at = created_at
        self.source = source


class User:
    def __init__(self, name, userid, link, img):
        self.name = name
        self.userid = userid
        self.link = link
        self.img = img


def get_feed(term="narendra modi"):
    return get_twitter_feed(term) + get_instagram_feed(term)


def get_twitter_feed(term="narendra modi"):
    t_results = twitter_api.GetSearch(term)
    results = []
    for res in t_results:
        owner_user = User(res.user.name, res.user.screen_name, res.user.url, res.user.profile_image_url)
        content = Content(res.text,
                          res.media[0]["media_url_https"] if (res.media and len(res.media) > 0) else "",
                          res.urls[0].url if (len(res.urls) > 0) else "",
                          owner_user,
                          res.created_at_in_seconds,
                          Source.TWITTER)
        results.append(content)
    return results


def get_instagram_feed(term="narendra modi"):
    return []
    recent_media, next_ = instagram_api.tag_recent_media(20, None, term.replace(" ", ""))
    # user_recent_media(user_id="userid", count=10)
    results = []
    for media in recent_media:
        results.append(media.caption.text)

    return results

# get_instagram_feed("morning")
# get_twitter_feed("narendra modi")
