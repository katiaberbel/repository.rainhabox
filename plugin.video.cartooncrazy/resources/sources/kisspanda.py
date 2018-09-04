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
import re
import time

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/kisspanda_net.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'https://kisspanda.net/'
query = base+'?s=%s'
useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)
    
def MAIN_MENU():
    
    list_item = xbmcgui.ListItem(label='Family Guy')
    list_item.setArt({'fanart':fanart,'thumb':base+'wp-content/uploads/2015/05/821.jpg'})
    url = get_url(source='KissPanda', endpoint=base+'family-guy-watch-online/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='The Simpsons')
    list_item.setArt({'fanart':fanart,'thumb':base+'wp-content/uploads/2015/05/1019.jpg'})
    url = get_url(source='KissPanda', endpoint=base+'the-simpsons-watch-online/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='American Dad')
    list_item.setArt({'fanart':fanart,'thumb':base+'wp-content/uploads/2016/01/4164.jpg'})
    url = get_url(source='KissPanda', endpoint=base+'american-dad-watch-online/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='South Park')
    list_item.setArt({'fanart':fanart,'thumb':base+'wp-content/uploads/2015/06/946.jpg'})
    url = get_url(source='KissPanda', endpoint=base+'south-park-watch-online/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Futurama')
    list_item.setArt({'fanart':fanart,'thumb':base+'wp-content/uploads/2015/05/828.jpg'})
    url = get_url(source='KissPanda', endpoint=base+'futurama-watch-online/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    image = soup.find('img',{'class':'attachment-full'})['src']
    item_lis = soup.find('article',{'class':'listCat'}).findAll('li')
    titles = [li.a['title'] for li in item_lis]
    links = [li.a['href'] for li in item_lis]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='KissPanda', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    iframes = soup.find('div',{'class':lambda x: x and 'post-single-content' in x.split()}).findAll('iframe')
    play_links = [iframe['src'] for iframe in iframes]
    titles = ['Link '+str(i+1) for i, iframe in enumerate(iframes)]
    
    dialog = xbmcgui.Dialog()
    ret = dialog.select('Choose a Stream', titles)
    if ret > -1:
        print play_links[ret]
        source_html = requests.get(play_links[ret])
        c = source_html.content
        if c.find('_url = "') > 0:
            l = c[c.find('_url = "')+8:c.find('"',c.find('_url = "')+9)]
            l = urllib.unquote(l).decode('utf8')
            print l
            if '.playpanda' in l:
                source_html = requests.get(l)
                c = source_html.content
            else:
                play_link = l
        if c.find('var video_links = ') > 0:
            try:
                video_link_object = c[c.find('var video_links = ')+18:c.find(';',c.find('var video_links = '))]
                video_links = json.loads(video_link_object)
                links = []
                for typ in video_links['normal']:
                    for vid in video_links['normal'][typ]:
                       links.append(vid['link'])
                link_list = []
                for l in links:
                    if urlresolver.HostedMediaFile(l).valid_url():
                       l = urlresolver.HostedMediaFile(l).resolve()
                       link_list.append(l)
                if link_list:
                    play_link = link_list[0]
                else:
                    play_link = links[0]
            except:
                play_link = link
    
        li = xbmcgui.ListItem('')
        li.setPath(play_link)
        xbmc.Player().play(play_link, li, False)
        quit()

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query % title)
        [td.extract() for td in soup.findAll('td',{'class':'txt_right'})]
        containers = soup.findAll('tr')[1:]
        if len(containers) == 0 and any(x for x in ['&' in title,'%26' in title]):
            new_term = title.replace('&','and').replace('%26','and')
            print '=====re-searching for ({}) on ({})====='.format(new_term,'kisspanda')
            soup = SOUPIFY(query % new_term)
            containers = soup.findAll('tr')[1:]
        print list(containers)
        titles = [regulate.unescape(tr.td.a.text+' [COLOR blue]KISSPANDA[/COLOR]') for tr in containers]
        links = [tr.td.a['href'] for tr in containers]
        images = [menu_icon for tr in containers]
        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if 'episode' in link: PLAY_VIDEO(link)
        elif link: CARTOON_EPISODES(link) 
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])