from BeautifulSoup import BeautifulSoup
from urlparse import parse_qsl
from urllib import urlencode
import urlresolver
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import base64
import urllib
import xbmc
import json
import sys
import os
import re

addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
_url = sys.argv[0]
_handle = int(sys.argv[1])
base = 'https://pastebin.com/raw/'
yt = 'plugin://plugin.video.youtube/play/?video_id=%s'

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SHOW_REQUESTS(url=base+'vx4yU0D4'):
    x = requests.get(url).text
    vids=re.compile('<item>(.+?)</item>', re.MULTILINE|re.DOTALL).findall(x)
    dirs=re.compile('<dir>(.+?)</dir>', re.MULTILINE|re.DOTALL).findall(x)
    if url == base+'vx4yU0D4':
        list_item = xbmcgui.ListItem(label='[COLOR yellow] + Request a Show or Movie + [/COLOR]')
        url = get_url(source='requestedtitles',request='request')
        xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    for dir in dirs:
        name = re.compile('<name>(.+?)</name>').findall(dir)[0]
        thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(dir)[0]
        link = re.compile('<link>(.+?)</link>').findall(dir)[0]
        list_item = xbmcgui.ListItem(label=name)
        list_item.setArt({'thumb':thumb})
        url = get_url(source='requestedtitles',endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    for vid in vids:
        title = re.compile('<title>(.+?)</title>').findall(vid)[0]
        thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(vid)[0]
        link = re.compile('<link>(.+?)</link>').findall(vid)[0]
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'thumb':thumb})
        list_item.setProperty('IsPlayable','true')
        url = yt % link.split('v=')[1]
        xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def REQUEST_TITLE():
    dialog = xbmcgui.Dialog()
    d = dialog.yesno('Have you checked #1','Have you tried using the Universal Search feature to find your movie/show?')
    if d:
        d = dialog.yesno('Have you checked #2','Have you manually looked through all sources?')
        if d:
            d = dialog.input('Enter Title Request', type=xbmcgui.INPUT_ALPHANUM)
            if d != '':
                res = requests.get(base64.b64decode('aHR0cHM6Ly9ob29rLmlvL2x1Y2lmZXJvbmtvZGkvcmVxdWVzdC10d2VldHk/dGl0bGU9')+d).text
                j_obj = json.loads(res)
                if j_obj['status'] == 'success':
                    d = dialog.ok('Submission Successful','Your title has successfully been submitted. You can follow @LuciferOnKodi to be notified when it is added to the Requested Section')
                elif 'too long' in j_obj['reason'] or 'already been requested' in j_obj['reason']:
                    d = dialog.ok('Submission Failed',j_obj['reason'])
                else:
                    d = dialog.ok('Submission Failed','Your title could not be submitted due to an unknown error. If this issue persists please report it to @LuciferOnKodi on Twitter.')
        else:
            d = dialog.ok('Haven\'t Checked #2','Please look through all available sources first as Universal Search can sometimes miss some obscure titles.')
    else:
        d = dialog.ok('Haven\'t Checked #1','Please try using the Universal Search feature to find your title first as it may already be provided via an existing source.')
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    request = params.get('request')
    if params:
        if link is not None: SHOW_REQUESTS(link)
        elif request is not None: REQUEST_TITLE()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        SHOW_REQUESTS()      
              
if __name__ == '__main__':
    router(sys.argv[2][1:])