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
menu_icon = xbmc.translatePath(path+'resources/images/watchcartoonsonline_eu.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://watchcartoonsonline.eu/'
query = base+'?s='
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)

def MAIN_MENU():
    soup = SOUPIFY(base)

    list_item = xbmcgui.ListItem(label='Ongoing Series')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonsOnline', endpoint=base+'tag/ongoing')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Cartoon Shows')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonsOnline', endpoint=base+'tag/cartoon-series')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Years')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonsOnline', endpoint=base+'years/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonsOnline', endpoint=base+'genres/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Latest Uploads')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonsOnline', endpoint=base)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    latest_uploads = soup.findAll('article')
    
    titles = [regulate.unescape(div.div.a['title']) for div in latest_uploads]
    images = [div.div.a.div.img['src'] for div in latest_uploads]
    links = [div.div.a['href'] for div in latest_uploads]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='WatchCartoonsOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_CATEGORIES(link):
    soup = SOUPIFY(link)
    genre_buttons = soup.findAll('button')
    
    titles = [regulate.unescape(button.a.text) for button in genre_buttons]
    links = [button.a['href'] for button in genre_buttons]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='WatchCartoonsOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SERIES(link):
    soup = SOUPIFY(link)
    series_container = soup.find('div',{'id':'content_box'})
    series_episodes = series_container.findAll('li')[:-2]
    image = series_container.find('img')['src']
    titles = [regulate.unescape(li.a.text) for li in series_episodes]
    links = [li.a['href'] for li in series_episodes]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='WatchCartoonsOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    pagination = soup.find('div',{'class':'pagination'})
    if pagination is not None:
        current_page_li = soup.find('li',{'class':'current'})
        last_page_li = pagination.findAll('li')[-1]
        if last_page_li is not None:
            current_page = 'http://watchcartoonsonline.eu/page/%s/' % current_page_li.span.text
            if current_page != last_page_li.a['href']:
                try:
                    next_page = current_page_li.nextSibling.a['href']
                    list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                    url = get_url(source='WatchCartoonsOnline', endpoint=next_page)
                    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
                except:
                    pass

def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    play_links = []
    titles = []
    jwplayers = soup.findAll('div',{'class':'jwplayer'})
    if len(jwplayers) > 0:
        players = [jwplayer.nextSibling.text for jwplayer in jwplayers]
        for p, player in enumerate(players):
            match=re.compile("""file:\s*["']([^"']+).+?label:\s*["']([^"']+)""").findall(player)
            for url, quality in match:
                play_links.append(url)
                titles.append('Server %s (%s)' % (str(p+1), quality))
    iframes = soup.findAll('iframe')
    if len(iframes) > 0:
        [play_links.append(iframe['src']) if iframe['src'].startswith('http')
         else play_links.append('http:'+iframe['src'])
         for iframe in iframes]
        for i, iframe in enumerate(iframes):
            titles.append('Offsite Link %s' % str(i+1))
    dialog = xbmcgui.Dialog()
    ret = dialog.select('Choose a Stream', titles)
    if ret > -1:
        play_link = play_links[ret]
        if urlresolver.HostedMediaFile(play_link).valid_url():
            try:
                play_link = urlresolver.HostedMediaFile(play_link).resolve()
            except:
                play_link = play_link
        li = xbmcgui.ListItem('')
        li.setPath(play_link)
        xbmc.Player().play(play_link, li, False)

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query+title)
        containers = soup.find('div',{'id':'content_box'}).findAll('a')
        if len(containers) == 0 and '&' in title:
            soup = SOUPIFY(query+title.replace('&','and'))
            containers = soup.find('div',{'id':'content_box'}).findAll('a')
        
        titles = [regulate.unescape(a['title']+' [COLOR blue]WATCHCARTOONSONLINE[/COLOR]') for a in containers]
        images = [a.div.img['src'] for a in containers if a.find('img') is not None]
        links = [a['href'] for a in containers]
        return zip(titles, images, links)
    except:
        link = []
        return links
        
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    if params:
        link = params.get('endpoint')
        if link == base: CARTOON_LIST(base)
        elif link.startswith(base+'page/'): CARTOON_LIST(link)
        elif link.startswith(base+'category/'): CARTOON_LIST(link)
        elif link.startswith(base+'tag/'): CARTOON_LIST(link)
        elif link.startswith(base+'genres/'): CARTOON_CATEGORIES(link)
        elif link.startswith(base+'years/'): CARTOON_CATEGORIES(link)
        elif link.startswith(base+'watch/'): PLAY_VIDEO(link)
        elif len(link) > len(base): CARTOON_SERIES(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()

if __name__ == '__main__':
    router(sys.argv[2][1:])