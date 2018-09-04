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
menu_icon = xbmc.translatePath(path+'resources/images/watchcartoononline_com.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'https://www.watchcartoononline.com/'
query = base+'search'
post_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br','Accept-Language':'en-US,en;q=0.8',
                'Content-Type':'application/x-www-form-urlencoded','Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)

def MAIN_MENU():
    soup = SOUPIFY(base)
    menu_items = soup.find('ul',{'class':'nav-bar'}).findAll('li')[1:]
    titles = [i.text for i in menu_items]
    links = [i.a['href'] for i in menu_items]
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='WatchCartoonOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    """
    list_item = xbmcgui.ListItem(label='Series')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonOnline', endpoint=base+'cartoon-list')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Movies')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='WatchCartoonOnline', endpoint=base+'movie-list')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    """
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    title_containers = soup.find('div',{'class':'ddmcc'}).findAll('li')
    titles = [regulate.unescape(li.a.text) for li in title_containers 
              if ' dubbed' not in li.a.text.lower() and ' subbed' not in li.a.text.lower()]
    links = [li.a['href'] for li in title_containers 
             if ' dubbed' not in li.a.text.lower() and ' subbed' not in li.a.text.lower()]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='WatchCartoonOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    image = soup.find('img',{'class':'img5'})['src']
    episode_containers = soup.findAll('div',{'class':'cat-eps'})
    titles = [regulate.unescape(div.a.text) for div in episode_containers]
    links = [div.a['href'] for div in episode_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='WatchCartoonOnline', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    play_links = []
    titles = []
    jwplayer = soup.find('div',{'class':'pcat-jwplayer'}).script.text
    if len(jwplayer) > 0:
        match=re.compile("""file:\s*["']([^"']+).+?\s*label:\s*["']([^"']+)""").findall(jwplayer)
        if len(match) == 0:
            match=re.compile("""file:\s*["']([^"']+)""").findall(jwplayer)
            for m, url in enumerate(match):
                play_links.append(url)
                titles.append('Link %s' % str(m+1))
        else:
            for m, (url, quality) in enumerate(match):
                play_links.append(url)
                titles.append('Link %s (%s)' % (str(m+1), quality))
    
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
        quit()

def SEARCH(title):
    try:
        links = []
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Referer':query,'Accept-Encoding': 'gzip, deflate, br'}
        print 'searching for the phrase %s in watchcartoononline'%title
        soup = BeautifulSoup(requests.post(query,headers=headers,data={'catara':title,'konuara':'series'}).content)
        containers = soup.find('ul',{'class':'items'}).findAll('li')
        print 'containers are '+str(list(containers))
        if len(containers) == 0 and any(x for x in ['&' in title,'%26' in title]):
            new_term = title.replace('&','and').replace('%26','and')
            print 'searching for the phrase %s in watchcartoononline'%new_term
            soup = BeautifulSoup(requests.post(query,headers=headers,data = {'catara':new_term,'konuara':'series'}).content)
            containers = soup.find('ul',{'class':'items'}).findAll('li')
        
        titles = [regulate.unescape(li.find('div',{'class':'recent-release-episodes'}).a.text+' [COLOR blue]WATCHCARTOONONLINE[/COLOR]') for li in containers]
        images = [li.div.a.img['src'] for li in containers]
        links = [li.div.a['href'] for li in containers]
        return zip(titles, images, links)
    except:
        link = []
        return links
    
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if link.endswith('/cartoon-list'): CARTOON_LIST(link)
        elif '/anime/' in link: CARTOON_EPISODES(link)
        elif link.endswith('/movie-list'): CARTOON_LIST(link)
        elif link.endswith('/dubbed-anime-list'): CARTOON_LIST(link)
        elif link.endswith('/subbed-anime-list'): CARTOON_LIST(link)
        elif link.endswith('/ova-list'): CARTOON_LIST(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()

if __name__ == '__main__':
    router(sys.argv[2][1:])