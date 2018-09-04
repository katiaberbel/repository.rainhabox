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
import xbmc
import sys
import os
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/kimcartoon_me.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
with open(xbmc.translatePath(path+'cookies.lwp'), "a") as f: file_var = f 
cookie_file = xbmc.translatePath(path+'cookies.lwp')
base = 'http://kimcartoon.me/'
query = base+'Search/Cartoon?keyword=%s'
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
    url = get_url(source='KimCartoon', endpoint=base+'CartoonList/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Latest Update')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KimCartoon', endpoint=base+'CartoonList/LatestUpdate')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Newest')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KimCartoon', endpoint=base+'CartoonList/Newest')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Ongoing')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KimCartoon', endpoint=base+'Status/Ongoing')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Most Popular')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KimCartoon', endpoint=base+'CartoonList/MostPopular')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='KimCartoon', endpoint=base+'CartoonList/', part='genres')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    image_headers = '|User-Agent=%s&Referer=%s&Cookie=%s' % (useragent, base, getCookiesString())
    containers = soup.findAll('div',{'class':'item'})
    titles = [regulate.unescape(div.a.span.text+' '+div.div.a.text) if div.find('div',{'class':'ep-bg'}) 
              else regulate.unescape(div.a.span.text) 
              for div in containers]
    images = [base+div.a.img['src'][1:]+image_headers if not '//' in div.a.img['src'] 
              else div.a.img['src']+image_headers
              for div in containers]
    links = [base+div.a['href'] for div in containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KimCartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRES(link):
    soup = SOUPIFY(link)
    container = soup.find('div',{'id':'rightside'}).findAll('div',{'class':'barContent'})[1]
    genres = container.findAll('a')
    titles = [regulate.unescape(a.text) for a in genres]
    links = [base+a['href'] for a in genres]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KimCartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    image_headers = '|User-Agent=%s&Referer=%s&Cookie=%s' % (useragent, base, getCookiesString())
    container = soup.find('table',{'class':'listing'}).findAll('a')
    titles = [regulate.unescape(a.text) for a in container]
    image = base+soup.find('div',{'id':'container'}).findAll('img')[0]['src']+image_headers
    links = [base+a['href'][1:] for a in container]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='KimCartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)
    
def CARTOON_LINKS(link):
    print link
    soup = SOUPIFY(link)
    container = soup.find('select',{'id':'selectServer'}).findAll('option')
    titles = [regulate.unescape(option.text) for option in container if option.text != 'KimCartoon Beta']
    links = [option['value'] for option in container if not option['value'].endswith('&s=beta')]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KimCartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    try:
        pagination = soup.find('ul',{'class':'pager'})
        if pagination is not None:
            current_page = int(pagination.find('li',{'class':'current'}).text)
            last_page = int(pagination.findAll('li')[-1].a['page'])
            if current_page != last_page:
                next_page = base+pagination.findAll('li')[-2].a['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='KimCartoon', endpoint=next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    except:
        pass

 
def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    video_container = soup.find('div',{'id':'divContentVideo'})
    try: play_link = video_container.iframe['src']
    except: play_link = video_container.video['src']
    
    if urlresolver.HostedMediaFile(play_link).valid_url():
        try: play_link = urlresolver.HostedMediaFile(play_link).resolve()
        except: play_link = play_link
    
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
        item_divs = soup.findAll('div',{'class':'item'})
        if len(item_divs) == 0 and '&' in title:
            soup = SOUPIFY(query % title.replace('&','and'))
            item_divs = soup.findAll('div',{'class':'item'})
        
        titles = [regulate.unescape(div.a.span.text+' up to '+div.div.a.text+' [COLOR blue]KIMCARTOON[/COLOR]') if div.find('div',{'class':'ep-bg'}) 
                  else regulate.unescape(div.a.span.text+' [COLOR blue]KIMCARTOON[/COLOR]') 
                  for div in item_divs]
        images = [base+div.a.img['src'][1:]+image_headers if not '//' in div.a.img['src'] 
                  else div.a.img['src']+image_headers
                  for div in item_divs]
        links = [base+div.a['href'][1:] for div in item_divs]
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
        if part == 'genres': CARTOON_GENRES(link)
        elif '&s=' in link: PLAY_VIDEO(link)
        elif '?id=' in link: CARTOON_LINKS(link)
        elif '/Cartoon/' in link: CARTOON_EPISODES(link)
        elif link.startswith(base): CARTOON_LIST(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])