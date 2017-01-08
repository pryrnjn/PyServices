import json
import requests
from abc import ABCMeta, abstractmethod, abstractproperty


class SourceName:
    TWITTER, INSTAGRAM = "twitter", "instagram"


class FeedSource:
    __metaclass__ = ABCMeta

    def __init__(self, term):
        self.term = term
        self.raw_results = None
        self.contents = None

    @abstractproperty
    def source(self):
        pass

    @abstractmethod
    def fetch_feed(self):
        pass

    @abstractmethod
    def build_content(self):
        pass

    def remove_duplicacy(self):
        pass

    def get_content(self):
        self.fetch_feed()  # populate raw_results
        self.remove_duplicacy()  # refine raw_results
        self.build_content()  # build list of Content to return
        return self.contents


class Twitter(FeedSource):
    @property
    def source(self):
        return SourceName.TWITTER

    def __init__(self, term):
        super(Twitter, self).__init__(term)
        import twitter
        self.api = twitter.Api(consumer_key='wZDNRfzFbdOs59J6D6H7rEhmW',
                               consumer_secret='PwAPmfI18yff8dt6ta1YRncgDH1hHmsUEo1oUyKiedlMJkCaH7',
                               access_token_key='124545778-HLphpuUHHgmei9o9pUXX0BAN1T4PT8QG7jvYYaYW',
                               access_token_secret='tUilFXaRYb5uQYlv9OXSGT97ZtVijkxyjBoW07kxXxYmY')
        self.results = None

    def fetch_feed(self):
        self.raw_results = self.api.GetSearch(self.term)

    def build_content(self):
        self.contents = list()
        for res in self.raw_results:
            owner_user = User(res.user.name,
                              res.user.screen_name,
                              self.build_user_link(res.user.screen_name),
                              res.user.profile_image_url)
            content = Content(res.text,
                              res.media[0].media_url_https if (res.media and len(res.media) > 0) else "",
                              self.build_content_link(res.user.screen_name, res.id_str),
                              owner_user,
                              res.created_at_in_seconds,
                              "",
                              SourceName.TWITTER)
            self.contents.append(content)

    def build_user_link(self, userid):
        return "https://twitter.com/" + userid

    def build_content_link(self, userid, statusid):
        return "https://twitter.com/" + userid + "/status/" + statusid


class Instagram(FeedSource):
    @property
    def source(self):
        return SourceName.INSTAGRAM

    def __init__(self, term):
        super(Instagram, self).__init__(term)

        self.access_token = "838346436.7334de0.9c346c16a42a4adeb4346a0b21149572"
        self.client_secret = "8438f728ca2944d086c119aca1fbce34"
        self.tag_search_url = "https://api.instagram.com/v1/tags/{tag}/media/recent?access_token={access_token}"

    def fetch_feed(self):
        # self.raw_results = self.api.tag_recent_media(20, None, self.term.replace(" ", ""))
        tags = self.term.split()
        self.raw_results = []  # assuming response wud be json array
        for tag in tags:
            url = self.tag_search_url.format(tag=tag, access_token=self.access_token)
            resp = requests.get(url)
            self.raw_results += json.loads(resp.content)["data"]

    def build_content(self):
        self.contents = list()
        for res in self.raw_results:
            owner_user = User(res.get("user", {}).get("full_name", ""),
                              res.get("user", {}).get("username", ""),
                              self.build_user_link(res.get("user", {}).get("username", "")),
                              res.get("user", {}).get("profile_picture", ""))
            content = Content(res.get("caption", {}).get("text", ""),
                              res.get("images", {}).get("standard_resolution", {}).get("url", ""),
                              res.get("link"),
                              owner_user,
                              int(res.get("created_time", "")),
                              "",
                              SourceName.INSTAGRAM)
            self.contents.append(content)

    def remove_duplicacy(self):
        super(Instagram, self).remove_duplicacy()
        unique_ids = set()
        temp_results = self.raw_results
        self.raw_results = []
        for i in range(0, len(temp_results)):
            record = temp_results[i]
            if record["id"] not in unique_ids:
                unique_ids.add(record["id"])
                self.raw_results.append(record)

    def build_user_link(self, userid):
        return "https://instagram.com/" + userid


class Content:
    def __init__(self, text, img, link, owner, created_at, html, source):
        self.text = text
        self.img = img
        self.link = link
        self.owner = owner
        self.created_at = created_at
        self.html = html
        self.source = source


class User:
    def __init__(self, name, userid, link, img):
        self.name = name
        self.userid = userid
        self.link = link
        self.img = img
