# -*- coding: utf-8 -*-
from itemadapter import is_item, ItemAdapter

import random
import base64
from at_bot.settings import PROXIES

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist("USER_AGENTS"))

    def process_request(self, request, spider):
        # print "**************************" + random.choice(self.agents)
        request.headers.setdefault("User-Agent", random.choice(self.agents))
        

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy["user_pass"] is not None:
            request.meta["proxy"] = "http://%s" % proxy["ip_port"]
            encoded_user_pass = base64.b64encode(proxy["user_pass"].encode("utf-8"))
            request.headers["Proxy-Authorization"] = (
                "Basic " + encoded_user_pass.decode()
            )
            print(
                "**************ProxyMiddleware have pass************" + proxy["ip_port"]
            )
        else:
            print(
                "**************ProxyMiddleware no pass************" + proxy["ip_port"]
            )
            request.meta["proxy"] = "http://%s" % proxy["ip_port"]