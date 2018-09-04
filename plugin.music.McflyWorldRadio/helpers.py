# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
import os
import sys
import shutil
import urllib2
import urllib
import re
import time
import zipfile
import ntpath
import plugintools
import socket
import sqlite3
import json
import api
from requests import Session

session = Session()
    
headers = {
            'User-Agent': '%s-%s' % (api.AddonId, api.AddonVersion),
            'Content-Type': 'application/json',
        }

post_dict = { }

def postData(UPLOAD_URL,post_dict):
    try:
        post_data = json.dumps(post_dict)
        req = urllib2.Request(UPLOAD_URL, post_data, headers)
        return urllib2.urlopen(req).read()
    except Exception as e:
        xbmc.log('*********************************************************************************************************************')
        xbmc.log(str(e))
        return "error"


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 ('+ api.Platform +'; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def FireDrive(url):
    if ('http://m.firedrive.com/file/' not in url) and ('https://m.firedrive.com/file/' not in url) and ('http://www.firedrive.com/file/' not in url) and ('http://firedrive.com/file/' not in url) and ('https://www.firedrive.com/file/' not in url) and ('https://firedrive.com/file/' not in url): return url ## contain with current url if not a filedrive url.
    #else:
    try:
        if 'https://' in url: url=url.replace('https://','http://')
        html=net.http_GET(url).content; #print html; 
        if ">This file doesn't exist, or has been removed.<" in html: return "[error]  This file doesn't exist, or has been removed."
        elif ">File Does Not Exist | Firedrive<" in html: return "[error]  File Does Not Exist."
        elif "404: This file might have been moved, replaced or deleted.<" in html: return "[error]  404: This file might have been moved, replaced or deleted."
        data={}; r=re.findall(r'<input\s+type="\D+"\s+name="(.+?)"\s+value="(.+?)"\s*/>',html);
        for name,value in r: data[name]=value
        #print data; 
        if len(data)==0: return '[error]  input data not found.'
        html=net.http_POST(url,data,headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0','Referer': url,'Host': 'www.firedrive.com'}).content
        r=re.search('<a\s+href="(.+?)"\s+target="_blank"\s+id=\'top_external_download\'\s+title=\'Download This File\'\s*>',html)
        if r: print urllib.unquote_plus(r.group(1)); return urllib.unquote_plus(r.group(1))
        else: return url+'#[error]'
    except: return url+'#[error]'

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create(api.CAPTION,"מוריד קבצים",'אנא המתן ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except Exception as e:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()

def wizdownload(url, dest, dp=None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create(api.CAPTION,"",' ', '[COLOR=green][B]מוריד את החבילה המבוקשת[/COLOR][/B]')
        dp.update(0)
        start_time = time.time()
        urllib.urlretrieve(url, dest, lambda nb, bs, fs: _wizpbhook(nb, bs, fs, dp, start_time))
     
def _wizpbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60)
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

def setListView(content):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
        if content=='list':
            xbmc.executebuiltin("Container.SetViewMode(450)")
        else:
            xbmc.executebuiltin("Container.SetViewMode(500)")
