# -*- coding: utf-8 -*-
from itemadapter import is_item, ItemAdapter

import random
import base64
from at_bot.settings import PROXIES

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