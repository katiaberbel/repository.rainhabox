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
import sys
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/b99_tv.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://www.b99.tv/'
query = base+'?s=%s&search=Search'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)
    
def MAIN_MENU():
    list_item = xbmcgui.ListItem(label='Cartoon List (All)')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='B99', endpoint=base+'videos_categories/cartoons/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Series')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='B99', endpoint=base+'videos_categories/series/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Studios')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='B99', endpoint=base+'videos_categories/studios/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    containers = soup.findAll('article')
    titles = [regulate.unescape(article.find('h3',{'class':'title'}).text) for article in containers]
    images = [article.div.a.img['src'] for article in containers]
    links = [article.div.a['href'] for article in containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='B99', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    try:
        pagination = soup.find('ul',{'class':'page-numbers'})
        if pagination is not None:
            next_page_li = pagination.findAll('li')[-1]
            if next_page_li is not None and 'Next' in next_page_li.a.text:
                next_page = next_page_li.a['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='B99', endpoint=next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    except:
        pass

 
def PLAY_VIDEO(link):
    video_page = requests.get(link).content
    match = re.compile("""playerInstance.setup\({\n*\s*file:\s*["']([^"']+)["'],\n*\s*image:\s*["']([^"']+)["'],\n*\s*width:\s*.+?,\n*\s*height:\s*.+?,\n*\s*title:\s*["']([^"']+)["']""").findall(video_page)
    for video, thumbnail, title in match:
        if video.endswith('%20'): play_link = video[:-3]
        else: play_link = video
        thumb = thumbnail
        video_name = title
    if urlresolver.HostedMediaFile(play_link).valid_url():
        try: play_link = urlresolver.HostedMediaFile(play_link).resolve()
        except: play_link = play_link
    li = xbmcgui.ListItem(video_name)
    li.setPath(play_link)
    li.setArt({'thumb':thumb})
    xbmc.Player().play(play_link, li, False)
    quit()

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query % title)
        containers = soup.findAll('article')
        if len(containers) == 0 and '&' in title:
            soup = SOUPIFY(query % title.replace('&','and'))
            containers = soup.findAll('article')
        titles = [regulate.unescape(article.find('h3',{'class':'title'}).text)+' [COLOR blue]B99[/COLOR]' for article in containers]
        images = [article.div.a.img['src'] for article in containers]
        links = [article.div.a['href'] for article in containers]
        
        for i, link in enumerate(links):
            list_item = xbmcgui.ListItem(label=titles[i])
            list_item.setArt({'thumb':images[i]})
            url = get_url(source='B99', endpoint=link)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        return zip(titles, images, links)
    except:
        link = []
        return links
    
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if '/videos_categories/' in link: CARTOON_LIST(link)
        elif '/video/' in link: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])