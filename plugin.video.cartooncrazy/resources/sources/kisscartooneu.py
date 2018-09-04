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
import urllib
import xbmc
import json
import sys
import os
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/kisscartoon_eu.png')
with open(xbmc.translatePath(path+'cookies.lwp'), "a") as f: file_var = f 
cookie_file = xbmc.translatePath(path+'cookies.lwp')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://kisscartoon.eu/'
query = base+'?s=%s'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
#useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36'
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
    url = get_url(source='KissCartoonEU', endpoint=base)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Cartoon Series')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonEU', endpoint=base+'tag/series/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Cartoon Movies')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonEU', endpoint=base+'category/movie/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Disney Cartoons')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonEU', endpoint=base+'list-of-disney-cartoons-movie-of-all-time/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KissCartoonEU', endpoint=base, part='genres')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    articles = soup.findAll('article')
    titles = [regulate.unescape(article.header.h2.a.text) for article in articles]
    images = [article.div.a.div.img['src']+'|User-Agent=%s&Referer=%s&Cookie=%s'%(useragent,base,getCookiesString()) 
              for article in articles]
    links = [article.div.a['href'] for article in articles]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonEU', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    episodes = soup.findAll('li',{'class':'list'})
    if len(episodes) == 0: PLAY_VIDEO(link)
    
    titles = [regulate.unescape(li.a.text) for li in episodes]
    links = [li.a['href'] for li in episodes]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KissCartoonEU', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRES(link):
    query_link = 'http://kisscartoon.eu/?cat='
    soup = SOUPIFY(link)
    genres = soup.find('select').findAll('option')[1:]
    titles = [regulate.unescape(option.text) for option in genres]
    links = [query_link+option['value'] for option in genres]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KissCartoonEU', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_DISNEY(link):
    soup = SOUPIFY(link)
    original = link
    title_lis = soup.find('ul',{'class':'lcp_catlist'}).findAll('li')
    titles = [regulate.unescape(li.a.text) for li in title_lis]
    links = [li.a['href'] for li in title_lis]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KissCartoonEU', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    if not original.endswith('lcp_page0=2#lcp_instance_0'):
        list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KissCartoonEU', endpoint=base+'list-of-disney-cartoons-movie-of-all-time/?lcp_page0=2#lcp_instance_0')
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    try:
        pagination = soup.findAll('div',{'class':'pagination'})[-1]
        if pagination is not None:
            next_page = pagination.find('i',{'class':'fa fa-angle-right'}).previous['href']
            if next_page is not None:
                try:
                    next_page = pagination.find('li',{'class':'current'}).nextSibling.a['href']
                    list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                    url = get_url(source='KissCartoonEU', endpoint=next_page)
                    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
                except:
                    pass
    except:
        pass

def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    l = soup.find('div',{'class':'videoWrapper'}).iframe['src']
    # l contains online3s.net link (http://online3s.net/embed-2/?vid=7Z7WZ6F)
    req = requests.get(l).content
    print req
    match = re.compile("""ajax_get_video_info":"(.+?)","ajax_video_report":"(.+?)""").findall(req)
    #Get variables for calls to ajax_url
    vid_id = l.split('=')[1]
    for info, report in match:
        ajax_get_video_info = info
        ajax_video_report = report
    
    action_one = 'ajax_get_video_info'
    action_two = 'ajax_video_report'
    
    ajax_url = 'http://online3s.net/wp-admin/admin-ajax.php?action=%s&vid_id=%s&nonce=%s'
    call_one = ajax_url % (action_one, vid_id, ajax_get_video_info) + '&server=1'
    call_two = ajax_url % (action_two, vid_id, ajax_video_report)
    call_three = ajax_url % (action_one, vid_id, ajax_get_video_info) + '&server=2'
    
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': l,'User-Agent':useragent,'Cookie':getCookiesString()}
    res1 = requests.post(call_one,headers=headers)
    res2 = requests.post(call_two,headers=headers)
    res3 = requests.post(call_three,headers=headers)
    file_obj = json.loads(res3.content)
    play_link = file_obj[0]['file']
    
    if urlresolver.HostedMediaFile(play_link).valid_url():
        try:
            play_link = urlresolver.HostedMediaFile(play_link).resolve()
        except:
            play_link = play_link
            
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
        articles = soup.findAll('article')
        if len(articles) == 0 and any(x for x in ['&' in title,'%26' in title]):
            new_term = title.replace('&','and').replace('%26','and')
            print '=====re-searching for ({}) on ({})====='.format(new_term,'kisscartooneu')
            soup = SOUPIFY(query % new_term)
            articles = soup.findAll('article')
        titles = [regulate.unescape(article.header.h2.a.text+' [COLOR blue]KISSCARTOONEU[/COLOR]') for article in articles]
        images = [article.div.a.div.img['src']+'|User-Agent=%s&Referer=%s&Cookie=%s'%(useragent,base,getCookiesString()) 
                  for article in articles]
        links = [article.div.a['href'] for article in articles]
        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    part = params.get('part')
    if params:
        if link == base and part is not None: CARTOON_GENRES(link)
        elif link == base: CARTOON_LIST(link)
        elif link.startswith(base+'page/'): CARTOON_LIST(link)
        elif link.startswith(base+'?cat='): CARTOON_LIST(link)
        elif link.startswith(base+'tag/series/'): CARTOON_LIST(link)
        elif link.startswith(base+'category/movie/'): CARTOON_LIST(link)
        elif link.startswith(base+'list-of-disney-cartoons-movie-of-all-time/'): CARTOON_DISNEY(link)
        elif link.startswith(base): CARTOON_EPISODES(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()      
              
if __name__ == '__main__':
    router(sys.argv[2][1:])