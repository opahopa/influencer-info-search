import sys
import collections


class Proxy(object):
    def __init__(self, ip_port, type):
        self.ip_port = ip_port
        self.type = type

    def dict_for_requests(self):
        if self.type is 'http':
            return dict(http='http://' + self.ip_port, https='https://' + self.ip_port)
        elif self.type is 'socks4':
            dict(http='socks4://' + self.ip_port, https='socks4://' + self.ip_port)
        elif self.type is 'socks5':
            dict(http='socks5://' + self.ip_port, https='socks5://' + self.ip_port)


class InfoResult(object):
    data = {
        'facebook': '',
        'twitter': '',
        'instagram': '',
        'linkedin': '',
        'other': []
    }

    def __init__(self, name, match_urls=None, domains=None, emails=None):
        self.name = name
        self.emails = emails
        self.other = []

        try:
            for url in match_urls:
                if "facebook" in url:
                    self.facebook = url
                elif "twitter" in url:
                    self.twitter = url
                elif "instagram" in url:
                    self.instagram = url
                elif "linkedin" in url:
                    self.linkedin = url
                else:
                    self.other.append(url)

            self.domains = domains

        except:
            print(sys.exc_info()[0])

    def to_csv_dict(self):
        try:
            if isinstance(self.other, collections.Iterable):
                self.other = '\n'.join(el for el in self.other)

            if isinstance(self.emails, collections.Iterable):
                self.emails = '\n'.join(el for el in self.emails)

            if isinstance(self.domains, collections.Iterable):
                # domains_temp = ['name: {}; created: {};'.format(el['name'], el['created']) for el in self.domains]
                domains_temp = [el['name'] for el in self.domains]
                self.domains = '\n'.join(map(str, domains_temp))


        except Exception as ex:
            print('exception on result dict creation: ' + ex)

        return self.__dict__
