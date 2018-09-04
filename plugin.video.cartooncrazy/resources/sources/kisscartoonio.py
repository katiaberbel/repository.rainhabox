from BeautifulSoup import BeautifulSoup
from resources.modules import *
from urlparse import parse_qsl
from urllib import urlencode
import urlresolver
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import json
import xbmc
import sys
import os
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/kisscartoon_io.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
file_var = open(xbmc.translatePath(path+'cookies.lwp'), "a")
cookie_file = xbmc.translatePath(path+'cookies.lwp')
base = 'https://kisscartoon.io/'
query = base+'Search/?s=%s'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
#useragent = 'Apple-iPhone/701.341'
request_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate','Referer':base,'Upgrade-Insecure-Requests':'1','User-Agent':useragent}
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    content = utils.getHtml(link)
    return BeautifulSoup(content)
    
def MAIN_MENU():
    
    list_item = xbmcgui.ListItem(label='Cartoon List (All)')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonIo', endpoint=base+'CartoonList/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Latest Update')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonIo', endpoint=base+'CartoonList/LatestUpdate')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Newest')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonIo', endpoint=base+'CartoonList/Newest')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Ongoing')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonIo', endpoint=base+'Status/Ongoing')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Most Popular')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonIo', endpoint=base+'CartoonList/MostPopular')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonIo', endpoint=base+'CartoonList/', part='genres')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    image_headers = '|User-Agent=%s&Referer=%s&Cookie=%s' % (useragent, base, getCookiesString())
    containers = soup.findAll('a',{'class':'item_movies_link'})
    titles = [regulate.unescape(a.text) for a in containers]
    img_containers = soup.findAll('img')[4:-1]
    images = [img['src'] for img in img_containers if not any([img['src'].endswith('newupdate.png'),img['src'].endswith('hot.png')])]
    [img.extract() for img in images if img.endswith('newupdate.png') or img.endswith('hot.png')]
    links = [a['href'] for a in containers]
    print list(images)
    print len(list(images))
    print len(list(links))
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i][6:])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})#menu_icon})
        url = get_url(source='KissCartoonIo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRES(link):
    soup = SOUPIFY(link)
    genres = soup.find('div',{'id':'rightside'}).findAll('h4',{'class':'tit'})
    titles = [regulate.unescape(h.a.text) for h in genres]
    links = [h.a['href'] for h in genres]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KissCartoonIo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    image_headers = '|User-Agent=%s&Referer=%s&Cookie=%s' % (useragent, base, getCookiesString())
    container = soup.findAll('h3')
    titles = [regulate.unescape(h.a.text[6:]) for h in container]
    image = soup.find('div',{'class':'a_center'}).img['src']+image_headers
    links = [h.a['href'] for h in container]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='KissCartoonIo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    try:
        pagination = soup.find('ul',{'class':'pager'})
        if pagination is not None:
            current_page = int(pagination.find('li',{'class':'current'}).text)
            last_page = int(pagination.findAll('li')[-2].a['href'].split('=')[-1])
            if current_page != last_page:
                next_page = pagination.findAll('li')[-1].a['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='KissCartoonIo', endpoint=next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    except:
        pass

 
def PLAY_VIDEO(link):
    j_call = '%sajax/anime/load_episodes?episode_id=%s'%(base, link.split('=')[-1])
    j_resp = SOUPIFY(j_call)
    j_obj = json.loads(str(j_resp))
    play_link = 'https:'+j_obj['value'].replace(';=','=')
    hs = {'Connection': 'keep-alive', 'Accept': 'application/json, text/javascript, */*; q=0.01', 
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
          'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.8'}
    content = utils.getHtml(play_link, link, hs)
    play_link = re.compile('{"file":"(.+?)"}').findall(content)[0].replace('\/','/')
    
    print play_link
    play_link += '|User-Agent=%s&Referer=%s' % (useragent, link)
    li = xbmcgui.ListItem('')
    li.setPath(play_link)
    xbmc.Player().play(play_link, li, False)
    quit()

def getCookiesString():
    cookieString=""
    import cookielib
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookie_file,ignore_discard=True)
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: 
        import sys,traceback
        traceback.print_exc(file=sys.stdout)
    return cookieString

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query % title)
        image_headers = '|User-Agent=%s&Referer=%s&Cookie=%s' % (useragent, base, getCookiesString())
        containers = soup.findAll('a',{'class':'item_movies_link'})
        if len(containers) == 0 and any(x for x in ['&' in title,'%26' in title]):
            new_term = title.replace('&','and').replace('%26','and')
            print '=====re-searching for ({}) on ({})====='.format(new_term,'kisscartoonio')
            soup = SOUPIFY(query % new_term)
            containers = soup.findAll('a',{'class':'item_movies_link'})
        
        titles = [regulate.unescape(a.text+' [COLOR blue]KISSCARTOONIO[/COLOR]').replace('Watch','') for a in containers]
        img_containers = soup.findAll('img')[4:-1]
        images = [img['src'] for img in img_containers if not any([img['src'].endswith('newupdate.png'),img['src'].endswith('hot.png')])]
        [img.extract() for img in images if img.endswith('newupdate.png') or img.endswith('hot.png')]
        links = [a['href'] for a in containers]
        print list(titles)
        return zip(titles, images, links)
    except:
        link = []
        return links
    
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    part = params.get('part')
    print link
    if params:
        if part == 'genres': CARTOON_GENRES(link)
        elif '?id=' in link: PLAY_VIDEO(link)
        elif '/Cartoon/' in link: CARTOON_EPISODES(link)
        elif link.startswith(base): CARTOON_LIST(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])