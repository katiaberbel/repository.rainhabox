from urlparse import parse_qsl
from urllib import urlencode
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import base64
import json
import xbmc
import sys

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.cartooncrazy')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
region = addon.getSetting("yt-reg")
key = addon.getSetting("pyt-key")
if key == "": 
    try: key = base64.b64decode(addon.getSetting("yt-key"))
    except: key = addon.getSetting("yt-key")
try: headers = {'Referer':base64.b64decode(addon.getSetting("yt-ref"))}
except: headers = {'Referer':addon.getSetting("yt-ref")}
blacklist = ['news','music','radio','nasa','chat']
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))
    
def STREAMS(link=None):
    if link is None:
        link = base64.b64decode('aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20veW91dHViZS92My9zZWFyY2g/'
                                'cGFydD1zbmlwcGV0JmV2ZW50VHlwZT1saXZlJnR5cGU9dmlkZW8mcT0yNC83'
                                'JTIwY2FydG9vbiZyZWdpb25Db2RlPXt9Jm1heFJlc3VsdHM9NTAma2V5PXt9').format(region, key)
    req = requests.get(link, headers=headers)
    if req.status_code == 200:
        res = json.loads(req.text)
        if not len(res['items']) == 0:
            for stream in res['items']:
                skip = False
                for word in blacklist:
                    if any(w in stream['snippet']['title'].lower() for w in [' '+word,word+' ']):
                        skip = True
                        break
                if skip: continue
                list_item = xbmcgui.ListItem(label=regulate.unescape(stream['snippet']['title'].encode("ascii", "ignore").encode('utf-8')))
                list_item.setArt({'fanart':fanart,'thumb':stream['snippet']['thumbnails']['high']['url']})
                list_item.setProperty('IsPlayable','true')
                l = base64.b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9JXM=') % stream['id']['videoId']
                xbmcplugin.addDirectoryItem(_handle, l, list_item, False)
            next_page = res.get('nextPageToken')
            if next_page:
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                call = base64.b64decode('aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20veW91dHViZS92My9zZWFyY2g/'
                                        'cGFydD1zbmlwcGV0JmV2ZW50VHlwZT1saXZlJnR5cGU9dmlkZW8mcT0yNC83'
                                        'JTIwY2FydG9vbiZyZWdpb25Db2RlPXt9Jm1heFJlc3VsdHM9NTAma2V5PXt9').format(region, key)
                url = get_url(source='Live247',endpoint=call+'&pageToken='+next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_handle)
    else:
        if req.status_code == 400 and 'unsupportedRegionCode' in req.text: 
            e = 'Stream unavailable in your region. Please change region code in settings and try again.'
        elif req.status_code == 429: 
            e = 'Too Many Requests, please wait a minute and try again.\nIf issue persists please add personal Youtube api key in settings.'
        elif req.status_code == 410:
            e = 'Stream has been taken down, please try another one.'
        elif req.status_code == 503: 
            e = 'Youtube Api is temporarily down, please try again in a bit.'
        else: 
            e = 'Unknown error occurred. Please try again later.'
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, e, 10000, icon))
        print req.text

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if link: STREAMS(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        STREAMS()      
              
if __name__ == '__main__':
    router(sys.argv[2][1:])