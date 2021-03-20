import os
import re
from requests import Session
import tempfile
import traceback
import urllib
import PySimpleGUI as sg

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd


class TwitSc:
    
    def __init__(self):
        self.USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        o = Options()
        o.add_argument('--no-sandbox')
        o.add_argument('user-agent=%s' % self.USER_AGENT)
        o.add_argument('--headless')
        o.add_argument('--disable-web-security')
        o.add_argument('--user-data-dir=%s' %tempfile.mktemp())
        o.add_argument('--allow-running-insecure-content')
        o.add_experimental_option('useAutomationExtension', False)
        o.add_experimental_option("excludeSwitches",["enable-automation"]);
        self.Twitter = webdriver.Chrome(options=o)
        self.GlobalWait = WebDriverWait(self.Twitter, 40)
        self.idregex = re.compile('^https://twitter.com/.*?/status/([0-9]*)$')

    def myprint(self, t):
        print(t)
        self.lines.append(t)
        self.window["-FILE LIST-"].update(self.lines)
        self.window.Refresh()

    def Run(self):
        self.lines = []
        file_list_column = [
            [
                sg.Text("Excel File"),
                sg.In(size=(45, 1), enable_events=True, key="-FILE-"),
                sg.FileBrowse(),
            ],
            [
                sg.Text("Output Folder"),
                sg.In(size=(40, 1), enable_events=True, key="-FOLDER-"),
                sg.FolderBrowse(),
            ],
            [
                sg.B(button_text="Start", enable_events=True,key="-GO-")
            ],
            [
                sg.Listbox(
                    values=self.lines, enable_events=True, size=(65, 30), key="-FILE LIST-"
                )
            ],
        ]
        layout = [
            [
                sg.Column(file_list_column),
            ]
        ]
        self.window = sg.Window("Twitter Screenshot", layout,size=(500, 500))
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == '-FILE-':
                self.FILE = values['-FILE-']
            if event == '-FOLDER-':
                self.FOLDER = values['-FOLDER-']
            if event == '-GO-':
                self._Run()

    def _Run(self):
        class m:
            def __init__(self, txt):
                self.txt = txt
            def __call__(self,driver):
                return self.txt not in driver.page_source
        tweets = pd.read_excel(self.FILE, engine='openpyxl')['Unnamed: 2'].tolist()
        s = Session()
        try:
            for i, tweet in enumerate(tweets):
                self.Twitter.set_window_size("2000", "2000")
                self.myprint('Processing %s (%s/%s)' % (tweet, i+1, len(tweets)))
                tweetId = self.idregex.findall(tweet)[0]
                r = s.get('https://publish.twitter.com/oembed?url=%s&dnt=1&hideConversation=on&partner=&hide_thread=true' % urllib.parse.quote(tweet))
                self.Twitter.get('data:text/html;charset=utf-8,%s' % r.json()['html'].replace('#', '%23'))
                el = self.GlobalWait.until(ec.presence_of_element_located((By.XPATH, '/html/body/blockquote')))
                self.GlobalWait.until(ec.staleness_of(el))
                frame = self.Twitter.find_element_by_xpath('//*[@id="twitter-widget-0"]')
                frameSize = frame.size
                self.GlobalWait.until(ec.frame_to_be_available_and_switch_to_it(frame))
                self.GlobalWait.until(m('background-color: rgb(204, 214, 221);'))
                self.Twitter.set_window_size(str(frameSize['width']+16), str(frameSize['height']+32))
                self.Twitter.save_screenshot(os.path.join(self.FOLDER, '%s.png' % tweetId))
        except:
            self.Twitter.save_screenshot(os.path.join(self.FOLDER,'error.png'))
            with open(os.path.join(self.FOLDER,'error.html'), 'w') as f:
                f.write(self.Twitter.page_source)
            self.myprint(traceback.format_exc())
        finally:
            try: self.Twitter.close()
            except: pass
            try: self.Twitter.quit()
            except: pass
            self.myprint('done')

if __name__ == '__main__':
    TwitSc().Run()
    