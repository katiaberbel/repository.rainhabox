from resources.modules import incapsula
from BeautifulSoup import BeautifulSoup
from urlparse import parse_qsl
from urllib import urlencode
import urlresolver
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import xbmc
import json
import sys
import re
import time

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/theseriesonline_net.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://theseriesonline.net/'
query = base+'movie/search/%s'
useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    session = incapsula.IncapSession()
    response = session.get(link)
    return BeautifulSoup(response)
    
def MAIN_MENU():
    filter = base+'movie/filter/all/all/animation/all/all/%s/'
    
    list_item = xbmcgui.ListItem(label='Latest')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='TheSeriesOnline', endpoint=filter % 'latest')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Most Viewed')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='TheSeriesOnline', endpoint=filter % 'most')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Top Imdb')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='TheSeriesOnline', endpoint=filter % 'imdb')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    original_link = link
    soup = SOUPIFY(link)
    item_divs = soup.findAll('div',{'class':'ml-item'})
    titles = [regulate.unescape(div.find('h2').text+' ('+div.find('span',{'class':'mli-quality'}).text+')')
              if div.find('span',{'class':'mli-quality'}) is not None 
              else regulate.unescape(div.find('h2').text+' (up to '+div.find('span',{'class':'mli-eps'}).text+')') 
              for div in item_divs]
    images = [div.img['data-original'] for div in item_divs]
    links = [base[:-1]+div.a['href'].replace('https','http')+'/watching.html' for div in item_divs]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='TheSeriesOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup, original_link)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    original_link = link
    soup = SOUPIFY(link)
    servers = soup.findAll('div',{'class':lambda x: x and 'le-server' in x.split()})
    s = soup.findAll('div',{'class':lambda x: x and 'les-title' in x.split()})
    sources = [div.text for div in s]
    titles = []
    links = []
    for i, server in enumerate(servers):
        episodes = server.findAll('a')
        titles.extend([regulate.unescape('%s (%s)'%(a['title'],sources[i])) for a in episodes])
        links += [a['player-data'] if a['player-data'].startswith('http') 
                  else 'http'+a['player-data'] if a['player-data'].startswith(':')
                  else 'http:'+a['player-data'] for a in episodes]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='TheSeriesOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup, original_link)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup, link):
    try:
        pagination = soup.find('ul',{'class':'pagination'})
        if pagination is not None:
            next_page = pagination.find('li',{'class':'active'}).nextSibling
            if not next_page is None:
                try:
                    next_page = link+next_page.a['href']
                    list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                    url = get_url(source='TheSeriesOnline', endpoint=next_page)
                    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
                except:
                    pass
    except:
        pass

def PLAY_VIDEO(link):
    if urlresolver.HostedMediaFile(link).valid_url():
        try:
            play_link = urlresolver.HostedMediaFile(link).resolve()
        except:
            play_link = link
    else:
        play_link = link
    play_link +='|User-Agent=%s&Referer=%s' % (useragent, base)
    
    li = xbmcgui.ListItem('')
    li.setPath(play_link)
    xbmc.Player().play(play_link, li, False)
    quit()

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query % title)
        item_divs = soup.findAll('div',{'class':'ml-item'})
        titles = [regulate.unescape(div.find('h2').text+' ('+div.find('span',{'class':'mli-quality'}).text+')')
                  if div.find('span',{'class':'mli-quality'}) is not None 
                  else regulate.unescape(div.find('h2').text+' (up to '+div.find('span',{'class':'mli-eps'}).text+')') 
                  for div in item_divs]
        images = [div.img['data-original'] for div in item_divs]
        links = [base[:-1]+div.a['href'].replace('https','http')+'/watching.html' for div in item_divs]

        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    print link
    if params:
        if link.endswith('watching.html'): CARTOON_EPISODES(link)
        elif link.startswith(base): CARTOON_LIST(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])