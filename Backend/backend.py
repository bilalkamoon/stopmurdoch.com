
import copy
import datetime
import http
import json
import os
import re
from requests.sessions import Session
import simplejson
import tempfile
import threading
import time
import traceback
import urllib
from zipfile import ZipFile

from flask import Flask
from flask import request
from flask import send_file
from flask.helpers import make_response
from flask_cors.extension import CORS
from marrow.mailer import Mailer, Message
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import Column, MetaData, String, Table, Boolean
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import twitter
import xlsxwriter

import numpy as np
import pandas as pd


app = Flask(__name__)
CORS(app, supports_credentials=True)

metadata = MetaData()
engine = create_engine('mysql+pymysql://%s:%s@localhost/%s' % ('[redacted]', urllib.parse.quote_plus('[redacted]'), '[redacted]'),pool_recycle=3600)
urls = Table('urls',metadata,
                  Column('keyy',String),
                  Column('url',String))
users = Table('users', metadata, Column('username', String),Column('password', String),Column('email', String), Column('isAdmin', Boolean))
global latestTimestamp
latestTimestamp = None
global latestDf
latestDf = None
global latestDfText
latestDfText = None

@app.route('/api/Import', methods = ['POST']) 
def Import():
    dbLocation = './database.pickle'
    eventsLocation = './events.pickle'
    eventsAssignLocation = './eventsAssign.pickle'
    subjectLocation = './subject.pickle'
    textLocation = './text.pickle'
    urlsLocation = './urls.pickle'
    
    dfOld = pd.read_pickle(dbLocation) if os.path.exists(dbLocation) else pd.DataFrame([])
    dfEventsOld = pd.read_pickle(eventsLocation) if os.path.exists(eventsLocation) else pd.DataFrame([])
    dfEventsAssignOld = pd.read_pickle(eventsAssignLocation)  if os.path.exists(eventsAssignLocation) else pd.DataFrame([])
    dfSubjectOld = pd.read_pickle(subjectLocation)  if os.path.exists(subjectLocation) else pd.DataFrame([])
    dfTextOld = pd.read_pickle(textLocation)  if os.path.exists(textLocation) else pd.DataFrame([])
    dfUrlsOld = pd.read_pickle(urlsLocation)  if os.path.exists(urlsLocation) else pd.DataFrame([])
    
    files = dict(request.files)
    file_ = next(iter(files.values()))
    file_.seek(0)
    tmpFile = tempfile.NamedTemporaryFile(mode='wb', suffix='.%s' % file_.filename.split('.')[-1])
    tmpFile.write(file_.read())
    dct = pd.read_excel(tmpFile.name, engine='openpyxl', sheet_name=['Core Data', 'Events Create', 'Event Assign', 'Subject', 'Text', 'Media URLs Assign'],
                            na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null'],
                            keep_default_na=False)
    tmpFile.close()
    df = dct['Core Data'].dropna(how='all').set_index('Media_Title')
    newDf = df.combine_first(dfOld)
    newDf.to_pickle(dbLocation)
    
    dfEvents = dct['Events Create'].dropna(how='all').set_index('Event_Description')
    dfEvents.combine_first(dfEventsOld).to_pickle(eventsLocation)
    
    dfEventsAssign = dct['Event Assign'].dropna(how='all')
    dfEventsAssign = pd.concat([dfEventsAssign, dfEventsAssignOld]).drop_duplicates()
    dfEventsAssign.to_pickle(eventsAssignLocation)
    
    dfSubject = dct['Subject'].dropna(how='all')
    dfSubject = pd.concat([dfSubject, dfSubjectOld]).drop_duplicates()
    dfSubject.to_pickle(subjectLocation)
    
    
    dfText = dct['Text'].dropna(how='all')
    dfText['Media_Text'] = dfText['Media_Text'].apply(lambda x: str(x).strip())
    dfText = pd.concat([dfText, dfTextOld]).drop_duplicates()
    dfText = dfText.drop(dfText.loc[dfText['Media_Title'] == ''].index)
    dfText.to_pickle(textLocation)
    
    dfUrls = dct['Media URLs Assign']
    dfUrls = pd.concat([dfUrls, dfUrlsOld]).drop_duplicates()
    dfUrls.to_pickle(urlsLocation)
    
    df, _ = __Load(df=newDf, dfText=dfText)
    formats, authors, publications, owners, countries, states, cities, events, subjects = __GetDropDowns(df, dfEvents, dfSubject)
    total = len(df)
    df = df.iloc[:10]
    if 'Media_File' in df.columns:
        urlsToShorten = df['Media_File'].to_dict()
        shortenedUrl = __Shorten(urlsToShorten)
        df['Media_File'] = pd.Series(shortenedUrl)
    df = df.reset_index()
    if len(df):
        df['Media_Date'] = pd.to_datetime(df['Media_Date']).dt.strftime("%d/%m/%Y")
        df['Media_Text'] = df['Media_Text'].apply(lambda l: '"%s"' % '","'.join(l) if len (l) else '')
    return make_response(simplejson.dumps({'events': events, 'subjects': subjects, 'cities': cities, 'states': states, 'countries': countries, 'owners': owners, 'publications': publications, 'authors': authors, 'formats': formats, 'total': total, 'data':df.to_dict(orient='records')}, ignore_nan=True), http.HTTPStatus.OK)

def __Shorten(urlsToShorten):
    flipped = {v:k for k,v in urlsToShorten.items()}
    shortned = {}
    connection = engine.connect()
    r = connection.execute(urls.select(None).where(urls.c.url.in_(flipped.keys())))
    rows = r.fetchall()
    for keyy, url in rows:
        shortned[flipped[url]] = 'smirko.cc/%s' % keyy
        urlsToShorten.pop(flipped[url])
    if urlsToShorten:
        s = Session()
        r = s.post('http://smirko.cc/index2shorten.php',data={'data':json.dumps(urlsToShorten)})
        shortned2 = json.loads(r.text)
        shortned2.update(shortned)
        return shortned2
    return shortned

def __Load(df=None, dfText=None):
    global latestTimestamp
    global latestDf
    global latestDfText
    
    if df is None:
        if os.path.exists('./database.pickle'):
            timestamp = os.path.getmtime('./database.pickle')
            if latestTimestamp is None or timestamp > latestTimestamp:
                df = pd.read_pickle('./database.pickle')
                dfText = pd.read_pickle('./text.pickle')
                df = df.astype('object')
                df['Media_Text'] = [[]]* len(df)
                if len(dfText) and 'Media_Title' in dfText and 'Media_Text' in dfText:
                    x = dfText.groupby(['Media_Title'])['Media_Text'].unique()
                    for i, j in x.iteritems():
                        try:
                            df.at[i, 'Media_Text'] = j.tolist()
                        except:
                            print(i)
                            raise
                latestDf = copy.deepcopy(df)
                latestDfText = dfText
                latestTimestamp = timestamp
            else:
                df = copy.deepcopy(latestDf)
                dfText = latestDfText
            
        else:
            df = pd.DataFrame([])
            dfText = pd.DataFrame([])
    else:
        df = df.astype('object')
        df['Media_Text'] = [[]]* len(df)
        if len(dfText) and 'Media_Title' in dfText and 'Media_Text' in dfText:
            x = dfText.groupby(['Media_Title'])['Media_Text'].unique()
            for i, j in x.iteritems():
                try:
                    df.at[i, 'Media_Text'] = j.tolist()
                except:
                    print(i)
                    raise
        latestDf = copy.deepcopy(df)
        latestDfText = dfText
        latestTimestamp = time.time()
    return df, dfText

@app.route('/api/Clear2', methods = ['POST']) 
def Clear2():
    S = sessionmaker(bind=engine)
    session = S()
    session.execute('''TRUNCATE TABLE urls''')
    session.commit()
    session.close()
    return make_response('',200)

@app.route('/api/Clear', methods = ['POST']) 
def Clear():
    df = (os.remove('./database.pickle') if os.path.exists('./database.pickle') else None)
    dfText = (os.remove('./text.pickle') if os.path.exists('./text.pickle') else None)
    dfEvents = (os.remove('./events.pickle') if os.path.exists('./events.pickle')  else None)
    dfEventsAssign = (os.remove('./eventsAssign.pickle') if os.path.exists('./eventsAssign.pickle') else None)
    dfSubject = (os.remove('./subject.pickle') if os.path.exists('./subject.pickle')  else None)
    dfUrls = (os.remove('./urls.pickle') if os.path.exists('./urls.pickle')  else None)
    return make_response('',200)

def __GetDropDowns(df, dfEvents, dfSubject):
    x = df['Media_Format'].unique() if 'Media_Format' in df else []
    formats = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    x = df['Media_Author'].unique() if 'Media_Author' in df else []
    authors = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    x = df['Media_Publication_ID'].unique() if 'Media_Publication_ID' in df else []
    publications = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    x = df['Media_Owner'].unique() if 'Media_Owner' in df else []
    owners = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    x = df['Media_Country'].unique() if 'Media_Country' in df else []
    countries = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    x = df['Media_State'].unique() if 'Media_State' in df else []
    states = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    x = df['Media_City'].unique() if 'Media_City' in df else []
    cities = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    events = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in dfEvents.index]))
    x = dfSubject['Media_Subject'].unique() if 'Media_Subject' in dfSubject else []
    subjects = list(set([i if isinstance(i, str) and i != '' else '(empty)' for i in x]))
    return formats, authors, publications, owners, countries, states, cities, events, subjects

@app.route('/api/GetData', methods = ['POST']) 
def GetData():
    page = int(request.form.get('page'))
    itemsPerPage = int(request.form.get('itemsPerPage'))
    title = request.form.get('title')
    selectedFormats = request.form.get('selectedFormats')
    selectedAuthors = request.form.get('selectedAuthors')
    selectedPublications = request.form.get('selectedPublications')
    selectedOwners = request.form.get('selectedOwners')
    selectedCountries = request.form.get('selectedCountries')
    selectedStates = request.form.get('selectedStates')
    selectedCities = request.form.get('selectedCities')
    selectedEvents = request.form.get('selectedEvents')
    selectedSubjects = request.form.get('selectedSubjects')
    singleDate = request.form.get('SingleDate')
    dateRange = request.form.get('DateRange')
    text = request.form.get('text')
    doExport = request.form.get('doExport') == 'true'
    doScreenshot = request.form.get('doScreenshot') == 'true'
    df, dfText = __Load()
    dfEvents = (pd.read_pickle('./events.pickle') if os.path.exists('./events.pickle') else pd.DataFrame([])) 
    dfEventsAssign = (pd.read_pickle('./eventsAssign.pickle') if os.path.exists('./eventsAssign.pickle') else pd.DataFrame([])) 
    dfSubject = (pd.read_pickle('./subject.pickle') if os.path.exists('./subject.pickle') else pd.DataFrame([])) 
    if not doExport and not doScreenshot:
        formats, authors, publications, owners, countries, states, cities, events, subjects = __GetDropDowns(df, dfEvents, dfSubject)
    multiCond = df.index
    if text and 'Media_Text' in dfText:
        multiCond = np.intersect1d(multiCond, dfText.loc[dfText['Media_Text'].str.lower().str.contains(text.lower()), 'Media_Title'].unique())
    if selectedEvents and 'Event_Description' in dfEventsAssign:
        selectedEvents = selectedEvents.split(',')
        isEmpty = '(empty)' in selectedEvents
        if isEmpty:
            selectedEvents += ['']
            subCond = dfEventsAssign['Event_Description'].isin(selectedEvents) | pd.isnull(dfEventsAssign['Event_Description'])
        else:
            subCond = dfEventsAssign['Event_Description'].isin(selectedEvents)
        multiCond = np.intersect1d(multiCond, dfEventsAssign.loc[subCond, 'Media_Title'].unique())
    if selectedSubjects and 'Media_Subject' in dfSubject:
        selectedSubjects = selectedSubjects.split(',')
        isEmpty = '(empty)' in selectedSubjects
        if isEmpty:
            selectedSubjects += ['']
            subCond = dfSubject['Media_Subject'].isin(selectedSubjects) | pd.isnull(dfSubject['Media_Subject'])
        else:
            subCond = dfSubject['Media_Subject'].isin(selectedSubjects)
        multiCond = np.intersect1d(multiCond, dfSubject.loc[subCond, 'Media_Title'].unique())
    df = df.loc[multiCond]
    cond = np.ones(len(df), dtype=bool)
    if title:
        cond = cond & df.index.str.lower().str.contains(title.lower())
    if selectedFormats:
        selectedFormats = selectedFormats.split(',')
        isEmpty = '(empty)' in selectedFormats
        if isEmpty:
            selectedFormats += ['']
            cond = cond & (df['Media_Format'].isin(selectedFormats) | pd.isnull(df['Media_Format']))
        else:
            cond = cond & (df['Media_Format'].isin(selectedFormats))
    if selectedAuthors:
        selectedAuthors = selectedAuthors.split(',')
        isEmpty = '(empty)' in selectedAuthors
        if isEmpty:
            selectedAuthors += ['']
            cond = cond & (df['Media_Author'].isin(selectedAuthors) | pd.isnull(df['Media_Author']))
        else:
            cond = cond & (df['Media_Author'].isin(selectedAuthors))
    if selectedPublications:
        selectedPublications = selectedPublications.split(',')
        isEmpty = '(empty)' in selectedPublications
        if isEmpty:
            selectedPublications += ['']
            cond = cond & (df['Media_Publication_ID'].isin(selectedPublications) | pd.isnull(df['Media_Publication_ID']))
        else:
            cond = cond & (df['Media_Publication_ID'].isin(selectedPublications))
    if selectedOwners:
        selectedOwners = selectedOwners.split(',')
        isEmpty = '(empty)' in selectedOwners
        if isEmpty:
            selectedOwners += ['']
            cond = cond & (df['Media_Owner'].isin(selectedOwners) | pd.isnull(df['Media_Owner']))
        else:
            cond = cond & (df['Media_Owner'].isin(selectedOwners))
    if selectedCountries:
        selectedCountries = selectedCountries.split(',')
        isEmpty = '(empty)' in selectedCountries
        if isEmpty:
            selectedCountries += ['']
            cond = cond & (df['Media_Country'].isin(selectedCountries) | pd.isnull(df['Media_Country']))
        else:
            cond = cond & (df['Media_Country'].isin(selectedCountries))
    if selectedStates:
        selectedStates = selectedStates.split(',')
        isEmpty = '(empty)' in selectedStates
        if isEmpty:
            selectedStates += ['']
            cond = cond & (df['Media_State'].isin(selectedStates) | pd.isnull(df['Media_State']))
        else:
            cond = cond & (df['Media_State'].isin(selectedStates))
    if selectedCities:
        selectedCities = selectedCities.split(',')
        isEmpty = '(empty)' in selectedCities
        if isEmpty:
            selectedCities += ['']
            cond = cond & (df['Media_City'].isin(selectedCities) | pd.isnull(df['Media_City']))
        else:
            cond = cond & (df['Media_City'].isin(selectedCities))
    if singleDate and singleDate != 'null':
        cond = cond & (df['Media_Date'] == pd.to_datetime(singleDate, format='%Y-%m-%d'))
    if dateRange and dateRange != 'null':
        dateRange1, dateRange2 =  dateRange.split(',')
        dateRange1, dateRange2 = pd.to_datetime(dateRange1, format='%Y-%m-%d'), pd.to_datetime(dateRange2, format='%Y-%m-%d')
        rangeFrom = min(dateRange1, dateRange2)
        rangeTo = max(dateRange1, dateRange2)
        cond = cond & ( rangeFrom <= df['Media_Date']) & (df['Media_Date'] <= rangeTo)
    df = df.loc[cond]
    if doExport:
        mediaText = df['Media_Text']
        dfToSave = df.drop('Media_Text', axis=1).reset_index()
        tmpFile = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx')
        workbook = xlsxwriter.Workbook(tmpFile.name, {'nan_inf_to_errors': True, 'default_date_format': 'dd-mm-yyyy', 'strings_to_urls': False})
        a, b, c = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color':  '#00b0f0', 'font_name': 'Calibri', 'font_size': 11}), workbook.add_format({'bold': False, 'font_color': 'black', 'font_name': 'Calibri', 'font_size': 11}), workbook.add_format({'bold': False, 'font_color': 'black', 'font_name': 'Calibri', 'font_size': 11, 'num_format': 'dd-mm-yyyy'})
        worksheet = workbook.add_worksheet('Core Data')
        __Save(worksheet, dfToSave.fillna('N/A'), a, b, c)
        dfEventsAssign = dfEventsAssign.loc[dfEventsAssign['Media_Title'].isin(df.index)]
        dfEvents = dfEvents.loc[dfEvents.index.isin(dfEventsAssign['Event_Description'])]
        worksheet = workbook.add_worksheet('Events Create')
        __Save(worksheet, dfEvents.reset_index(), a, b, c)
        worksheet = workbook.add_worksheet('Event Assign')
        __Save(worksheet, dfEventsAssign, a, b, c)
        #subject
        dfSubject = dfSubject.loc[dfSubject['Media_Title'].isin(df.index)]
        worksheet = workbook.add_worksheet('Subject')
        __Save(worksheet, dfSubject, a, b, c)
        
        mediaText = mediaText.apply(pd.Series).stack().reset_index(level=-1, drop=True).reset_index().rename(columns={0: 'Media_Text'})
        worksheet = workbook.add_worksheet('Text')
        __Save(worksheet, mediaText, a, b, c)
        
        # media urls assign
        dfUrls = (pd.read_pickle('./urls.pickle') if os.path.exists('./urls.pickle') else pd.DataFrame([])) 
        dfUrls = dfUrls.loc[dfUrls['Media_Title'].isin(df.index)]
        worksheet = workbook.add_worksheet('Media URLs Assign')
        __Save(worksheet, dfUrls, a, b, c)
        
        workbook.close()
        return send_file(tmpFile.name)
    elif doScreenshot:
        df = df.iloc[:500]
        o = Options()
        o.add_argument('--no-sandbox')
        o.add_argument('user-agent=%s' % 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
        o.add_argument('--headless')
        o.add_argument('--disable-web-security')
        o.add_argument('--user-data-dir=%s' %tempfile.mktemp())
        o.add_argument('--allow-running-insecure-content')
        o.add_experimental_option('useAutomationExtension', False)
        o.add_experimental_option("excludeSwitches",["enable-automation"]);
        Twitter = webdriver.Chrome(options=o)
        GlobalWait = WebDriverWait(Twitter, 40)
        idregex = re.compile('https://twitter.com/.*?/status/([0-9]*)$')
        class m:
            def __init__(self, txt):
                self.txt = txt
            def __call__(self,driver):
                return self.txt not in driver.page_source
        tweets = df.index
        s = Session()
        with tempfile.TemporaryDirectory() as tmpdirname:
            zipObj = ZipFile(os.path.join(tmpdirname, 'screenshots.zip'), 'w')
            try:
                for tweet in tweets:
                    tweet = '_'.join(tweet.split('_')[1:])
                    Twitter.set_window_size("2000", "2000")
                    tweetId = idregex.findall(tweet)[0]
                    r = s.get('https://publish.twitter.com/oembed?url=%s&dnt=1&hideConversation=on&partner=&hide_thread=true' % urllib.parse.quote(tweet))
                    Twitter.get('data:text/html;charset=utf-8,%s' % r.json()['html'].replace('#', '%23'))
                    el = GlobalWait.until(ec.presence_of_element_located((By.XPATH, '/html/body/blockquote')))
                    GlobalWait.until(ec.staleness_of(el))
                    frame = Twitter.find_element_by_xpath('//*[@id="twitter-widget-0"]')
                    frameSize = frame.size
                    GlobalWait.until(ec.frame_to_be_available_and_switch_to_it(frame))
                    GlobalWait.until(m('background-color: rgb(204, 214, 221);'))
                    Twitter.set_window_size(str(frameSize['width']+16), str(frameSize['height']+32))
                    Twitter.save_screenshot(os.path.join(tmpdirname, '%s.png' % tweetId))
                    zipObj.write(os.path.join(tmpdirname, '%s.png' % tweetId), '%s.png' % tweetId)
            except:
                print(traceback.format_exc())
            finally:
                try: Twitter.close()
                except: pass
                try: Twitter.quit()
                except: pass
                zipObj.close()
            return send_file(os.path.join(tmpdirname, 'screenshots.zip'))
    else:
        total = len(df)
        if itemsPerPage:
            df = df.iloc[(page -1) * itemsPerPage:page* itemsPerPage]
        if 'Media_File' in df.columns:
            urlsToShorten = df['Media_File'].to_dict()
            shortenedUrl = __Shorten(urlsToShorten)
            df['Media_File'] = pd.Series(shortenedUrl)
        df = df.reset_index()
        if len(df):
            df['Media_Date'] = pd.to_datetime(df['Media_Date']).dt.strftime("%d/%m/%Y")
            df['Media_Text'] = df['Media_Text'].apply(lambda l: '"%s"' % '","'.join(l) if len (l) else '')
        return make_response(simplejson.dumps({'events': events, 'subjects': subjects, 'cities': cities, 'states': states, 'countries': countries, 'owners': owners, 'publications': publications, 'authors': authors, 'formats': formats, 'total': total, 'data':df.to_dict(orient='records')}, ignore_nan=True), http.HTTPStatus.OK)

def __Save(worksheet, dfToSave, a, b, d):
    for c, col in enumerate(dfToSave.columns):
        width = max([len(str(s))*1.2 for s in dfToSave[col].values] + [len(col)*1.2])
        worksheet.set_column(c, c, width)
        worksheet.write(0, c, dfToSave.columns[c], a)
    for r in range(len(dfToSave.index)):
        for c in range(len(dfToSave.columns)):
            v1 = dfToSave.iat[r, c]
            if isinstance(v1, pd._libs.tslibs.timestamps.Timestamp):
                worksheet.write_datetime(r + 1, c, v1.to_pydatetime(), d)
            else:
                worksheet.write(r + 1, c, v1, b)

@app.route('/api/Login', methods = ['POST']) 
def Login():
    username = request.form.get('username')
    password = request.form.get('password')
    connection = engine.connect()
    r = connection.execute(users.select(None).where(users.c.username == username))
    row = r.fetchone()
    if row is None:
        return make_response({'error': 'Username does not exist'}, 200)
    if row.password != password:
        return make_response({'error': 'Wrong password'}, 200)
    return make_response({'data': row.isAdmin}, 200)

@app.route('/api/GetAccounts', methods = ['POST']) 
def GetAccounts():
    df = pd.read_csv('./accounts.csv', index_col=0)
    accounts = df['Account'].tolist()
    return make_response({'accounts': accounts}, 200)

@app.route('/api/GetUsers', methods = ['POST']) 
def GetUsers():
    connection = engine.connect()
    r = connection.execute(users.select(None))
    rows = r.fetchall()
    return make_response({'users': [{'Username': row.username, 'Password': row.password, 'Email': row.email, 'isAdmin': row.isAdmin} for row in rows]}, 200)

@app.route('/api/DeleteUser', methods = ['POST']) 
def DeleteUser():
    username = request.form.get('username')
    connection = engine.connect()
    connection.execute(users.delete(None).where(users.c.username == username))
    return make_response('',200)

@app.route('/api/UpdateUser', methods = ['POST']) 
def UpdateUser():
    user = json.loads(request.form.get('user'))
    connection = engine.connect()
    if 'OldUsername' in user:
        connection.execute(users.delete(None).where(users.c.username == user['OldUsername']))
    connection.execute(users.insert(None).values(username=user['Username'],password=user['Password'],email=user['Email'],isAdmin=user['isAdmin']))
    return make_response('',200)

@app.route('/api/UpdateAccounts', methods = ['POST']) 
def UpdateAccounts():
    accounts = request.form.get('accounts').split(',')
    df = pd.DataFrame(columns=['Account'], data=accounts)
    df.to_csv('./accounts.csv')
    return make_response('',200)

def goAsync():
    try:
        df =     pd.read_csv('./accounts.csv', index_col=0)
        accountNames  = [x.split('@')[-1] for x in df['Account'].tolist()]     
        tapi= twitter.Api(consumer_key='[redacted]', consumer_secret='[redacted]',
                          application_only_auth=True, tweet_mode='extended')
        tmpFile = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx')
        tmpFile2 = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx')
        workbook = xlsxwriter.Workbook(tmpFile.name, {'nan_inf_to_errors': True, 'default_date_format': 'dd-mm-yyyy', 'strings_to_urls': False})
        workbook2 = xlsxwriter.Workbook(tmpFile2.name, {'nan_inf_to_errors': True, 'default_date_format': 'dd-mm-yyyy', 'strings_to_urls': False})
        a, b = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color':  '#00b0f0', 'font_name': 'Calibri', 'font_size': 11}), workbook.add_format({'bold': False, 'font_color': 'black', 'font_name': 'Calibri', 'font_size': 11})
        a2, b2, d2 = workbook2.add_format({'bold': True, 'font_color': 'black', 'bg_color':  '#00b0f0', 'font_name': 'Calibri', 'font_size': 11}), workbook2.add_format({'bold': False, 'font_color': 'black', 'font_name': 'Calibri', 'font_size': 11}), workbook2.add_format({'bold': False, 'font_color': 'black', 'font_name': 'Calibri', 'font_size': 11, 'num_format': 'dd-mm-yyyy'})
        columns = ['Tweet Id', 'Text', 'Name', 'Screen Name', 'Created At', 'Media URLs']
        coreData = workbook2.add_worksheet('Core Data')
        mediaUrls = workbook2.add_worksheet('Media URLs Assign')
        mediaText = workbook2.add_worksheet('Text')
        coreDataCols = ['Media_Title', 'Media_Format', 'Media_Author', 'Media_Publication_ID', 'Media_Owner', 'Media_Country', 'Media_State', 'Media_City', 'Media_Date', 'Media_File']
        for c, col in enumerate(coreDataCols):
            width = min(8.43, len(col)*1.2)
            coreData.set_column(c, c, width)
            coreData.write(0, c, col, a2)
        mediaUtlsCols = ['Media_Title', 'Media_URLs']
        for c, col in enumerate(mediaUtlsCols):
            width = min(8.43, len(col)*1.2)
            mediaUrls.set_column(c, c, width)
            mediaUrls.write(0, c, col, a2)
        mediaTextCols = ['Media_Title', 'Media_Text']
        for c, col in enumerate(mediaTextCols):
            width = min(8.43, len(col)*1.2)
            mediaText.set_column(c, c, width)
            mediaText.write(0, c, col, a2)
        curIdx2 = 1
        curIdx3 = 1
        curIdx4 = 1
        for accountName in accountNames:
            worksheet = workbook.add_worksheet(accountName)
            for c, col in enumerate(columns):
                width = min(8.43, len(col)*1.2)
                worksheet.set_column(c, c, width)
                worksheet.write(0, c, col, a)
            max_id = None
            curIdx = 1
            while True:
                try:
                    tweets = tapi.GetUserTimeline(screen_name=accountName, count=200, include_rts=False,trim_user=False,exclude_replies=True, max_id=max_id if max_id is None else max_id-1)
                except:
                    break
                if len(tweets) == 0:
                    break
                for tweet in tweets:
                    max_id = tweet.id
                    ddatetime = datetime.datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y") 
                    ddate = ddatetime.strftime('%Y-%m-%d')
                    mediaTitle = '%s_https://twitter.com/%s/status/%s' %(ddate, accountName, tweet.id)
                    coreData.write(curIdx2, 0, mediaTitle, b2)
                    coreData.write(curIdx2, 1, "Twitter", b2)
                    coreData.write(curIdx2, 2, tweet.user.name, b2)
                    coreData.write_datetime(curIdx2, 8, ddatetime, d2)
                    coreData.write(curIdx2, 9, 'https://www.digbybamford/Tweets/'+ mediaTitle, b2)
                    curIdx2 += 1
                    worksheet.write(curIdx, 0, str(tweet.id), b)
                    mediaText.write(curIdx4, 0, mediaTitle,b)
                    if tweet.tweet_mode == 'extended':
                        worksheet.write(curIdx, 1, tweet.full_text, b)
                        mediaText.write(curIdx4, 1, tweet.full_text,b)
                    else:
                        worksheet.write(curIdx, 1, tweet.text, b)
                        mediaText.write(curIdx4, 1, tweet.text,b)
                    curIdx4 += 1
                    worksheet.write(curIdx, 2, tweet.user.name, b)
                    worksheet.write(curIdx, 3, accountName, b)
                    worksheet.write(curIdx, 4, tweet.created_at, b)
                    if tweet.media is not None:
                        for i, media in enumerate(tweet.media):
                            worksheet.write(curIdx, 5+i, media.media_url_https, b)
                            mediaUrls.write(curIdx3, 0, mediaTitle, b2)
                            mediaUrls.write(curIdx3, 1, media.media_url_https, b2)
                            curIdx3 += 1
                    curIdx += 1
        workbook.close()
        workbook2.close()
        zipObj = ZipFile('./tweets.zip', 'w')
        zipObj.write(tmpFile.name, 'Tweets.xlsx')
        zipObj.write(tmpFile2.name, 'CoreData.xlsx')
        zipObj.close()
        mailer = Mailer(dict(
            transport = dict(
                    use = 'smtp',
                    host = 'localhost')))
        mailer.start()
#         message = Message(author="[redacted]", to="[redacted]")
#         message.subject = "Twitter Result"
#         message.plain = " "
#         message.attach('./tweets.zip')
#         mailer.send(message)
        message = Message(author="[redacted]", to="[redacted]")
        message.subject = "Twitter Result"
        message.plain = " "
        message.attach('./tweets.zip')
        mailer.send(message)
        message = Message(author="[redacted]", to="[redacted]")
        message.subject = "Twitter Result"
        message.plain = " "
        message.attach('./tweets.zip')
        mailer.send(message)
        mailer.stop()
    except:
        mailer = Mailer(dict(
            transport = dict(
                    use = 'smtp',
                    host = 'localhost')))
        mailer.start()
        message = Message(author="[redacted]", to="[redacted]")
        message.subject = "Twitter Result"
        message.plain = traceback.format_exc()
        mailer.send(message)
        message = Message(author="[redacted]", to="[redacted]")
        message.subject = "Twitter Result"
        message.plain = "An error occured, the details have been sent to the developer."
        mailer.send(message)
        message = Message(author="[redacted]", to="[redacted]")
        message.subject = "Twitter Result"
        message.plain = "An error occured, the details have been sent to the developer."
        mailer.send(message)
        mailer.stop()

@app.route('/api/Twitter', methods = ['POST']) 
def Twitter():
    t = threading.Thread(target=goAsync)
    t.start()
    return make_response({'success':'success'},200)

@app.route('/api/News', methods = ['POST']) 
def News():
    files = dict(request.files)
    file_ = next(iter(files.values()))
    file_.seek(0)
    tmpFile = tempfile.NamedTemporaryFile(mode='wb', suffix='.%s' % file_.filename.split('.')[-1])
    tmpFile.write(file_.read())
    df = pd.read_excel(tmpFile.name, engine='openpyxl', header=None, names=['a','b','c', 'd','e','f','g','h','i','j','k'])
    tmpFile.close()
    s = Session()
    with tempfile.TemporaryDirectory() as tmpdirname:
        zipObj = ZipFile(os.path.join(tmpdirname, 'news.zip'), 'w')
        for row in df.itertuples():
            r = s.get('http://%s' % row.d, allow_redirects=True)
            if r.status_code != 200:
                continue
            with open(os.path.join(tmpdirname, row.k), 'wb') as f:
                f.write(r.content)
            zipObj.write(os.path.join(tmpdirname, row.k), row.k)
#             time.sleep(1)
        zipObj.close()
        return send_file(os.path.join(tmpdirname, 'news.zip'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
