#! python3

import requests
from bs4 import BeautifulSoup as bs
from send_sms import send_sms as sm
import time
import datetime

WAIT_HOURS = 23
SECS_HOUR = 60*60

class clbot(object):
    def __init__(self, url, outfile, txt_file, search=None, outgoing=None):

        self.urls = url if search is None else [url + '&query=' + s + '&sort=rel' for s in search]
        self.links = self.get_links_from_txt(txt_file)
        self.outgoing = outgoing
        start_time = datetime.datetime.now()
        id = []
        for i in range(WAIT_HOURS):
            last_link = self.get_links(txt_file)
            tmp_id = self.send_latest(last_link)
            if tmp_id is not None:
                id.append(tmp_id)
            time.sleep(SECS_HOUR)
            print("Test Run: current Time {0} \n in hour #{1}".format(datetime.datetime.now(), i))

        f = open(outfile, 'a')
        msg = 'CraigsList Bot Ran at: {0} \n Found {1} new msgs: \n'.format(start_time, len(id))
        f.write(msg)
        for i, j in enumerate(id):
            f.write('Msg_{0}_sent_id: {1}\n'.format(i, j))
        f.write('Ending time: {}\n'.format(datetime.datetime.now()))
        f.close()

    def get_links(self, link_file):
        last = None
        for url in self.urls:
            rsp = requests.get(url)
            page = bs(rsp.text, 'html.parser')
            items = page.find_all('item')
            for post in items[::-1]:
                link = post.get('rdf:about')
                link += '\n'
                if link not in self.links:
                    f = open(link_file, 'a')
                    f.write(link+'\n')
                    self.links.append(link)
                    last = link
        return last

    def get_links_from_txt(self, file):
        f = open(file, 'r')
        return f.readlines()

    def send_latest(self, link):
        mesg_id = None
        if link is not None:
            msg = 'BEEP BOOP BEEP BOOP Im Bruces Craigslisst Bot \n ' \
                                                'Hey Look at this Cannabis Job Posting in Eugene: \n' + link
            mesg_id = []
            for rec in self.outgoing:
                mesg_id.append(sm(msg, rec))
        return mesg_id

cl = clbot('https://eugene.craigslist.org/search/jjj?format=rss',
           'clbot_out.txt',
           'links.txt',
           search=['cannabis','budtender', 'trimmer', 'marijuana'], outgoing=['+15747804125', '+13174319944'])


