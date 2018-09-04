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
import json
import sys
import re
import time

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/gostream_is.png')
with open(xbmc.translatePath(path+'cookies.lwp'), "a") as f: file_var = f 
cookie_file = xbmc.translatePath(path+'cookies.lwp')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'https://gostream.is/'
query = base+'movie/search/%s'
useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    #return BeautifulSoup(requests.get(link).content)
    content = utils.getHtml(link)
    return BeautifulSoup(content)
    
def MAIN_MENU():
    filter = base+'movie/filter/all/%s/120/all/all/all/all'
    
    list_item = xbmcgui.ListItem(label='Latest')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='GoStream', endpoint=filter % 'latest')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Most Viewed')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='GoStream', endpoint=filter % 'view')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Most Favorited')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='GoStream', endpoint=filter % 'favorite')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Highest Rating')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='GoStream', endpoint=filter % 'rating')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Top Imdb')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='GoStream', endpoint=filter % 'imdb_mark')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    item_divs = soup.findAll('div',{'class':'ml-item'})
    titles = [regulate.unescape(div.find('h2').text+' '+div.find('span',{'class':'mli-quality'}).text)
              if div.find('span',{'class':'mli-quality'}) is not None 
              else regulate.unescape(div.find('h2').text+' '+div.find('span',{'class':'mli-eps'}).text) 
              for div in item_divs]
    images = [div.img['data-original'] for div in item_divs]
    links = [base+'ajax/movie_episodes/%s' % div['data-movie-id'] for div in item_divs]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='GoStream', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = BeautifulSoup(json.loads(utils.getHtml(link))['html'])
    servers = soup.findAll('div',{'class':lambda x: x and 'server-item' in x.split()})
    titles = []
    links = []
    
    for server in servers:
        episodes = server.findAll('a')
        titles.extend([regulate.unescape(a['title']+ ' (%s)' % server.div.text) for a in episodes])
        links.extend([link.split('?')[0]+'?ep=%s' % a['data-id'] for a in episodes])
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='GoStream', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    try:
        pagination = soup.find('ul',{'class':'pagination'})
        if pagination is not None:
            next_page = pagination.find('li',{'class':'next'})
            if next_page is not None:
                try:
                    next_page = next_page.a['href']
                    list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                    url = get_url(source='GoStream', endpoint=next_page)
                    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
                except:
                    pass
    except:
        pass

def PLAY_VIDEO(link):
    movie_token_url = base+'ajax/movie_token?eid=%s&mid=%s&_=%s'
    movie_source_url = base+'ajax/movie_sources/%s?x=%s&y=%s'
    movie_embed_url = base+'ajax/movie_embed/%s'
    eid = link.split('=')[-1]
    mid = link.split('/')[-1].split('?')[0]
    epoch_time = int(time.time())
    token_call = movie_token_url % (eid, mid, epoch_time)
    res = utils.getHtml(token_call)#requests.get(token_call).content
    match = re.compile("_x='(.+?)', _y='(.+?)';").findall(res)
    for _x, _y in match:
        x = _x
        y = _y
    source_call = movie_source_url % (eid, x, y)
    res = utils.getHtml(source_call)#requests.get(source_call).content
    if len(res) == 0: res = utils.getHtml(movie_embed_url%eid)#requests.get(movie_embed_url%eid).content
    final_result = re.compile('\"file\":\"(.+?)\"').findall(res)
    if len(final_result) == 0: final_result = re.compile('\"src\":\"(.+?)\"').findall(res)
    play_link = final_result[0].replace('\/','/') + '|User-Agent=%s&Referer=%s' % (useragent, link)
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
        soup = SOUPIFY(query % title)
        item_divs = soup.findAll('div',{'class':'ml-item'})
        if len(item_divs) == 0 and '&' in title:
            soup = SOUPIFY(query % title.replace('&','and'))
            item_divs = soup.findAll('div',{'class':'ml-item'})
        titles = [regulate.unescape(div.find('h2').text+' '+div.find('span',{'class':'mli-quality'}).text+' [COLOR blue]GOSTREAM[/COLOR]')
                  if div.find('span',{'class':'mli-quality'}) is not None 
                  else regulate.unescape(div.find('h2').text+' '+div.find('span',{'class':'mli-eps'}).text+' [COLOR blue]GOSTREAM[/COLOR]') 
                  for div in item_divs]
        images = [div.img['data-original'] for div in item_divs]
        links = [base+'ajax/movie_episodes/%s' % div['data-movie-id'] for div in item_divs]
        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if '/filter/' in link: CARTOON_LIST(link)
        elif '?ep=' in link: PLAY_VIDEO(link)
        elif 'ajax/movie_episodes/' in link: CARTOON_EPISODES(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()
              
if __name__ == '__main__':
    router(sys.argv[2][1:])