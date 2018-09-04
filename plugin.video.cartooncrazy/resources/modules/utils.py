#-*- coding: utf-8 -*-
__scriptname__ = "Cartoon Crazy"
__author__ = "@LuciferOnKodi"
__scriptid__ = "plugin.video.cartooncrazy"
__credits__ = "Alpha, Mort, Js, Jokstergfx, Mk"
__version__ = "1.1.54"

import urllib
import urllib2
import re
import cookielib
import os.path
import sys
import time
import tempfile
import sqlite3
import urlparse
import base64
from StringIO import StringIO
import gzip
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import cloudflare

#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = {'User-Agent': USER_AGENT,'Accept': '*/*','Connection': 'keep-alive'}

addon_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
icon = addon.getAddonInfo('icon')
path = 'special://home/addons/%s/' % addon_id
cookiePath = xbmc.translatePath(path+'cookies.lwp')
cj = cookielib.LWPCookieJar(cookiePath)
urlopen = urllib2.urlopen
Request = urllib2.Request
handlers = [urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler()]

if (2, 7, 8) < sys.version_info < (2, 7, 12):
    try:
        import ssl; ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        handlers += [urllib2.HTTPSHandler(context=ssl_context)]
    except:
        pass

if cj != None:
    if os.path.isfile(cookiePath):
        try:
            cj.load()
        except:
            try:
                os.remove(cookiePath)
                pass
            except:
                print 'Oh oh, The Cookie file is locked, please restart Kodi'
                pass
    cookie_handler = urllib2.HTTPCookieProcessor(cj)
    handlers += [cookie_handler]

opener = urllib2.build_opener(*handlers)
opener = urllib2.install_opener(opener)

def notify(header=None, msg='', duration=5000):
    if header is None: header = 'Cartoon Crazy'
    builtin = "XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon)
    xbmc.executebuiltin(builtin)

def kodilog(logvar):
    xbmc.log(str(logvar))

def getHtml(url, referer='', hdr=None, NoCookie=None, data=None):
    try:
        if not hdr:
            req = Request(url, data, headers)
        else:
            req = Request(url, data, hdr)
        if len(referer) > 1:
            req.add_header('Referer', referer)
        if data:
            req.add_header('Content-Length', len(data))
        response = urlopen(req, timeout=60)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            f.close()
        else:
            data = response.read()
        if not NoCookie:
            # Cope with problematic timestamp values on RPi on OpenElec 4.2.1
            try:
                cj.save(cookiePath)
            except: pass
        response.close()
    except urllib2.HTTPError as e:
        data = e.read()
        if e.code == 503 and 'cf-browser-verification' in data:
            data = cloudflare.solve(url,cj, USER_AGENT)
        else:
            raise urllib2.HTTPError()
    except Exception as e:
        if 'SSL23_GET_SERVER_HELLO' in str(e):
            notify('Oh oh','Python version to old - update to Krypton or FTMC')
            raise urllib2.HTTPError()
        else:
            notify('Oh oh','It looks like this website is down.')
            raise urllib2.HTTPError()
        return None
    return data


def postHtml(url, form_data={}, headers={}, compression=True, NoCookie=None):
    try:
        _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                      '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
        req = urllib2.Request(url)
        if form_data:
            form_data = urllib.urlencode(form_data)
            req = urllib2.Request(url, form_data)
        req.add_header('User-Agent', _user_agent)
        for k, v in headers.items():
            req.add_header(k, v)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        response = urllib2.urlopen(req)
        data = response.read()
        if not NoCookie:
            try:
                cj.save(cookiePath)
            except: pass
        response.close()
    except Exception as e:
        if 'SSL23_GET_SERVER_HELLO' in str(e):
            print 'Oh oh, Python version to old - update to Krypton or FTMC'
            raise urllib2.HTTPError()
        else:
            print 'Oh oh, It looks like this website is down.'
            raise urllib2.HTTPError()
        return None
    return data


def getHtml2(url):
    req = Request(url)
    response = urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data

def cleantext(text):
    text = text.replace('&amp;','&')
    text = text.replace('&#8211;','-')
    text = text.replace('&ndash;','-')
    text = text.replace('&#038;','&')
    text = text.replace('&#8217;','\'')
    text = text.replace('&#8216;','\'')
    text = text.replace('&#8230;','...')
    text = text.replace('&quot;','"')
    text = text.replace('&#039;','`')
    text = text.replace('&ntilde;','ñ')
    text = text.replace('&rsquo;','\'')
    return text

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext