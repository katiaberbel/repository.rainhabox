from BeautifulSoup import BeautifulSoup
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

addon = xbmcaddon.Addon(id='plugin.video.cartooncrazy')
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
_url = sys.argv[0]
_path = addon.getAddonInfo('path')
_handle = int(sys.argv[1])
regulate = HTMLParser.HTMLParser()
base = 'http://www.watchcartoons.com/'
ua_for_links = 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
mobile_ua = {'User-Agent': 'Apple-iPhone/701.341',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-type': 'application/x-www-form-urlencoded',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Upgrade-Insecure-Requests': '1',
                   'Connection': 'Keep-Alive'
              }

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    content = requests.get(link, headers=mobile_ua).content
    return BeautifulSoup(content)
    
def MAIN_MENU():
    list_item = xbmcgui.ListItem(label='Ongoing Cartoons')
    list_item.setArt({'thumb':icon,'fanart':fanart})
    url = get_url(source='WatchCartoons', endpoint=base+'ongoing/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Cartoon List')
    list_item.setArt({'thumb':icon,'fanart':fanart})
    url = get_url(source='WatchCartoons', endpoint=base+'content/list/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Movie List')
    list_item.setArt({'thumb':icon,'fanart':fanart})
    url = get_url(source='WatchCartoons', endpoint=base+'movies/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='By Genre')
    list_item.setArt({'thumb':icon,'fanart':fanart})
    url = get_url(source='WatchCartoons', endpoint=base+'content/genre/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Latest Episodes')
    list_item.setArt({'thumb':icon,'fanart':fanart})
    url = get_url(source='WatchCartoons', endpoint=base+'latest/episodes/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LATEST(link):
    soup = SOUPIFY(link)
    lis = soup.find('ul',{'class':'latest-list'}).findAll('li')
    titles = [li.find('div',{'class':'last-left'}).text for li in lis]
    links = [li.div.a['href'] for li in lis]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'thumb':icon,'fanart':fanart})
        url = get_url(source='WatchCartoons', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    next_page = soup.find('div',{'class':'pagination'})
    if next_page:
        pages = next_page.find('span').text.split(' of ')
        if int(pages[0]) < int(pages[1]):
            list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
            list_item.setArt({'thumb':icon,'fanart':fanart})
            url = get_url(source='WatchCartoons', endpoint=base+'latest/episodes/'+pages[0])
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)
    
def CARTOON_GENRES(link):
    soup = SOUPIFY(link)
    containers = soup.findAll('ul',{'class':'cartoon-list'})[-1].findAll('li')[1:]
    genres = [regulate.unescape(li.a.text) for li in containers]
    links = [li.a['href'] for li in containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=genres[i])
        list_item.setArt({'thumb':icon,'fanart':fanart})
        url = get_url(source='WatchCartoons', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRE(link):
    soup = SOUPIFY(link)
    containers = soup.find('div',{'class':'box-list'}).findAll('div',{'class':'box loading  '})
    titles = [regulate.unescape(div.find('a',{'class':'b-name'}).text) for div in containers]
    images = [div.find('a',{'class':'b-image'}).img['src'] for div in containers]
    links = [div.a['href'] for div in containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'thumb':images[i],'fanart':fanart})
        url = get_url(source='WatchCartoons', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_ONGOING(link):
    soup = SOUPIFY(link)
    containers = soup.find('div',{'class':'box-list'}).findAll('div',{'class':'box'})
    
    titles = [regulate.unescape(div.find('a',{'class':'b-name'}).text) for div in containers]
    image = []
    try: images = [div.find('a',{'class':'b-image'}).img['src'] for div in containers]
    except: 
        images = []
        for div in containers:
            try: images.append(div.find('div',{'class':'bp-image'}).img['src'])
            except: images.append('')
    links = [div.a['href'] for div in containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'thumb':images[i],'fanart':fanart})
        url = get_url(source='WatchCartoons', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    titles = []
    links = []
    containers = soup.find('div',{'class':'cl-left'}).findAll('li')
    [titles.append(regulate.unescape(li.a.text)) for li in containers if not li.a.text in titles]
    [links.append(li.a['href']) for li in containers if not li.a['href'] in links]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'thumb':icon,'fanart':fanart})
        url = get_url(source='WatchCartoons', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    try: match = re.compile("""var vid = document.getElementById\('html5_video'\);\n*\s*vid.src\s*=\s*['"](.+?)['"]""").findall(str(soup))[0]
    except:
        try: match = soup.find('param',{'name':'movie'})['value']
        except: 
            if 'Currently not Available' in str(soup):
                dialog = xbmcgui.Dialog()
                d = dialog.ok('Unavailable','This title is not available at this time')
                quit()
            else: match = None
    if match: PLAY_VIDEO(match, link)
    else:
        
        container = soup.findAll('ul',{'class':'cartoon-list'})[-1].findAll('li')
        titles = [regulate.unescape(li.a.text) for li in container]
        image = soup.find('div',{'class':'detail-cover'}).a.img['src']
        links = [li.a['href'] for li in container]
        
        for i, link in enumerate(links):
            list_item = xbmcgui.ListItem(label=titles[i])
            list_item.setArt({'thumb':image,'fanart':fanart})
            url = get_url(source='WatchCartoons', endpoint=link)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_handle)

 
def PLAY_VIDEO(link, referer):
    if not re.match('^http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+?',link) and not 'media=' in link:
        h = {'User-Agent': 'Apple-iPhone/701.341',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Content-type': 'application/x-www-form-urlencoded',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Upgrade-Insecure-Requests': '1',
                       'Connection': 'Keep-Alive'
                  }
        link_page = requests.get(link, allow_redirects=False, headers=h).content
        try: init = re.compile('<param name="movie" value="(.+?)"').findall(link_page)[0]
        except: init = re.compile('vid.src = "(.+?)";').findall(link_page)[0]
        if not re.match('.+?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+?',init) or 'googlevideo' in init:
            post_init = urllib.unquote(init).split('media=')[1]

            if 'blogspot' in post_init or 'googlevideo' in post_init:
                post_init = urllib.unquote(post_init).replace('||','|').split('|')
                titles = []
                links = []
                for i in post_init:
                    if len(i)<5: titles.append(i)
                    else: links.append(i)
                dialog = xbmcgui.Dialog()
                ret = dialog.select('Choose a Stream', titles)
                if ret > -1:
                    link = links[ret]
            else:
                link = post_init
        else:
            link = init
    elif 'media=' in link:
        post_init = urllib.unquote(link).split('media=')[1]

        if 'blogspot' in post_init or 'googlevideo' in post_init:
            post_init = urllib.unquote(post_init).replace('||','|').split('|')
            titles = []
            links = []
            for i in post_init:
                if len(i)<5: titles.append(i)
                else: links.append(i)
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Choose a Stream', titles)
            if ret > -1:
                link = links[ret]
        else:
            link = post_init
        
    
    play_link = urllib.unquote(link).replace('&amp;','&')+'|User-Agent=%s&Referer=%s'%(ua_for_links,referer)
    print play_link
    if urlresolver.HostedMediaFile(play_link).valid_url():
        try:
            play_link = urlresolver.HostedMediaFile(play_link).resolve()
        except:
            play_link = play_link
    
    li = xbmcgui.ListItem('')
    li.setPath(play_link)
    xbmc.Player().play(play_link, li, False)
    quit()

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    print link
    if params:
        if '/watch/' in link: CARTOON_EPISODES(link)
        elif link.startswith(base+'movies/'): CARTOON_ONGOING(link)
        elif link.startswith(base+'content/list/'): CARTOON_LIST(link)
        elif link.startswith(base+'ongoing/'): CARTOON_ONGOING(link)
        elif link.startswith(base+'content/genre/'): CARTOON_GENRES(link)
        elif link.startswith(base+'category/'): CARTOON_GENRE(link)
        elif link.startswith(base+'latest/'): CARTOON_LATEST(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])