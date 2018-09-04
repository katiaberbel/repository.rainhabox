from urlparse import parse_qsl
from urllib import urlencode
import urlresolver
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import urllib
import base64
import xbmc
import json
import sys
import os

addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/Alluc Search.png')
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
_url = sys.argv[0]
_handle = int(sys.argv[1])
time = 8000

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def Universal():
    dialog = xbmcgui.Dialog()
    d = dialog.ok('Universal Search','Note: See Settings for list of sources that are currently enabled for universal search. Also, this search may not always find all titles, so it\'s best to double-check within the individual sections.')
    d = dialog.input('Enter search term', type=xbmcgui.INPUT_ALPHANUM)
    if d != '':
        #!!!Search Form Submission Issues!!!from resources.sources import watchcartoononline
        #!!!Search Form Submission Issues!!!results = watchcartoononline.SEARCH(d)
        print 'search term from dialog box is '+d
        srcs = []
        from resources.modules import workers
        results = workers.Sites().search(d)
        for i, (title, image, link) in enumerate(results):
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'fanart':fanart,'thumb':image})
            s = title[title.find(']')+1:title.rfind('[')].lower()
            if s not in srcs: srcs.append(s)
            url = get_url(source=s,endpoint=link)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        print 'Total Source relevant to this search '+str(len(srcs))+' out of 15'
        print 'Source names '+str(list(srcs))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_handle)

def Alluc(query=None, start=0):
    default_key = addon.getSetting("al-key")
    per_page = addon.getSetting("pal-rpp")
    auth_type = addon.getSetting("al-type")
    auth_user = addon.getSetting("pal-user")
    auth_pass = addon.getSetting("pal-pass")
    auth_key = addon.getSetting("pal-key")
    if all([auth_type == 'User/Pass',auth_user != '',auth_pass != '']): 
        auth = 'user=%s&password=%s' % (auth_user, auth_pass)
    elif auth_type == 'Api Key' and auth_key != '': 
        auth = 'apikey=%s' % auth_key
    else:
        if start==0:
            dialog = xbmcgui.Dialog()
            d = dialog.ok('Alluc Search', 'Please consider adding your own user credentials or personal Api key in order to lighten the load on the public key, which can only request 5000 links/day. Using your own account will also allow you to adjust the number of results per page.')
        if default_key.startswith('1') and default_key.endswith('4'):
            auth = 'apikey=%s' % default_key
        else:
            auth = 'apikey=%s' % base64.b64decode(default_key)
        per_page = "15"
    alluc = base64.b64decode('aHR0cDovL3d3dy5hbGx1Yy5lZS9hcGkvc2VhcmNoL3N0cmVhbS8/'
                             'e30mcXVlcnk9e30mbmFtZTotJTIyeHh4JTIyJm5hbWU6LSUyMnBv'
                             'cm4lMjImbmFtZTotJTIyc2V4JTIyJm5hbWU6LSUyMmZ1Y2slMjIm'
                             'bmFtZTotJTIyYW5hbCUyMiZuYW1lOi0lMjJwdXNzeSUyMiZuYW1l'
                             'Oi0lMjJwZW5pcyUyMiZuYW1lOi0lMjJ2YWdpbmElMjImbmFtZTot'
                             'JTIyYmxvd2pvYiUyMiZuYW1lOi0lMjJoYW5kam9iJTIyJm5hbWU6'
                             'LSUyMmRpbGRvJTIyJm5hbWU6LSUyMmN1bSUyMiZjb3VudD17fSZm'
                             'cm9tPXt9')
    if query is None:
        dialog = xbmcgui.Dialog()
        query = dialog.input('Enter search term', type=xbmcgui.INPUT_ALPHANUM)
        if query != '':
            #authorization, search term, items per page, start from
            alluc_req = alluc.format(auth,urllib.quote(query),per_page,str(start))
        else:
            quit()
    else:
        alluc_req = alluc.format(auth,urllib.quote(query),per_page,str(start))
    req = requests.get(alluc_req)
    j_obj = json.loads(req.text)
    for result in j_obj['result']:
        list_item = xbmcgui.ListItem(label='%s [%s]' % (result['title'],result['hostername']))
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        link = result['hosterurls'][0]['url']
        url = get_url(source='Search',endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    if int(start) < int(j_obj['resultcount']):
        list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='Search',search='Alluc',query=query,start=int(start)+int(per_page))
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def RESOLVE(link):
    if urlresolver.HostedMediaFile(link).valid_url():
        play_link = urlresolver.HostedMediaFile(link).resolve()
        li = xbmcgui.ListItem('')
        li.setPath(play_link)
        xbmc.Player().play(play_link, li, False)
        quit()
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Unresolveable and/or Dead link. Please try another.', time, icon))

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    search = params.get('search')
    link = params.get('endpoint')
    query = params.get('query')
    start = params.get('start')
    if params:
        if link is not None: RESOLVE(link)
        elif search == 'Universal': Universal()
        elif query is not None: Alluc(query, start)
        elif search == 'Alluc': Alluc()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        SHOW_REQUESTS()      
              
if __name__ == '__main__':
    router(sys.argv[2][1:])