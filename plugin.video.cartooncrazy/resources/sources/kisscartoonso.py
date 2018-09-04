from BeautifulSoup import BeautifulSoup
from resources.modules import jsunpack
from urlparse import parse_qsl
from urllib import urlencode
import urlresolver
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import base64
import xbmc
import sys
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/kisscartoon_so.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://kisscartoon.so'
query = base+'/?s='
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)

def MAIN_MENU():
    soup = SOUPIFY(base)
    menu_items = soup.find('ul', {'class': 'main-header'}).findAll('li')[1:-1]
    categories = [regulate.unescape(menu_item.a.text) for menu_item in menu_items]
    category_links = [menu_item.a['href'] if menu_item.a['href'].startswith('http') 
                      else base+menu_item.a['href'] 
                      for menu_item in menu_items]
    for i, link in enumerate(category_links):
        list_item = xbmcgui.ListItem(label=categories[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_MOVIES(link):
    soup = SOUPIFY(link)
    video_titles = soup.findAll('div',{'class':'title'})
    movie_articles = soup.findAll('article', {'class': 'item movies'})
    quality_spans = soup.findAll('span',{'class':'quality'})
    
    titles = [regulate.unescape(video_title.text) for video_title in video_titles]
    qualities = [' ('+span.text+')' for span in quality_spans]
    titles = [title+qualities[titles.index(title)] for title in titles]
    images = [article.div.a.img['src'] for article in movie_articles]
    links = [article.div.a['href'] for article in movie_articles]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
       
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SERIES(link):
    soup = SOUPIFY(link)
    video_titles = soup.findAll('div',{'class':'title'})
    series_articles = soup.findAll('article', {'class': 'item tvshows'})
    
    titles = [regulate.unescape(video_title.text) for video_title in video_titles]
    images = [article.div.a.img['src'] for article in series_articles]
    links = [article.div.a['href'] for article in series_articles]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SERIES_SEASONS(link):
    soup = SOUPIFY(link)
    season_titles = soup.findAll('article', {'class': 'item se seasons'})
    season_images = soup.findAll('div', {'class': 'poster'})
    
    titles = [regulate.unescape(div.img['alt']) for div in season_images]
    images = [div.img['src'] for div in season_images]
    links = [div.div.div.a['href'] for div in season_titles]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SERIES_SEASON(link):
    soup = SOUPIFY(link)
    episode_titles = soup.findAll('div', {'class': 'episodiotitle'})
    episode_images = soup.findAll('div', {'class': 'imagen'})
    series_title = soup.find('div', {'class': 'data'}).h1.text
    
    titles = [regulate.unescape(div.b.a.text.replace(series_title,'')) for div in episode_titles]
    images = [div.a.img['src'] for div in episode_images]
    links = [div.b.a['href'] for div in episode_titles]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)
    
def CARTOON_SERIES_EPISODES(link):
    soup = SOUPIFY(link)
    try:
        series_title = soup.find('div', {'class': 'data'}).h1.text
        episode_titles = soup.findAll('div', {'class': 'episodiotitle'})
        episode_images = soup.findAll('div', {'class': 'imagen'})
        titles = [regulate.unescape(div.b.a.text.replace(series_title,'')) for div in episode_titles]
        images = [div.a.img['src'] for div in episode_images]
        links = [div.b.a['href'] for div in episode_titles]
    except:
        episode_titles = soup.findAll('article', {'class': 'item se episodes'})
        episode_images = soup.findAll('div', {'class': 'poster'})
        titles = [regulate.unescape(div.img['alt']+' ('+div.find('span', {'class': 'quality'}).text+')') for div in episode_images]
        images = [div.img['src'] for div in episode_images]
        links = [div.div.a['href'] for div in episode_images]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def TOP_IMDB():
    soup = SOUPIFY('http://kisscartoon.so/top-imdb/')
    video_divs = soup.findAll('div',{'class':'top-imdb-item'})
    
    titles = [regulate.unescape(div.find('div',{'class':'title'}).a.text) for div in video_divs]
    images = [div.find('div',{'class':'poster'}).a.img['src'] for div in video_divs]
    links = [div.find('div',{'class':'poster'}).a['href'] for div in video_divs]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='KissCartoonSo', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    pagination = soup.find('div',{'class':'pagination'})
    if pagination is not None:
        current_page = int(soup.find('span',{'class':'current'}).text)
        last_page = int(pagination.span.text.split(' of ')[1])
        if current_page != last_page:
            next_page = soup.find('div',{'class':'resppages'}).findAll('a')[-1]['href']
            list_item = xbmcgui.ListItem(label='[COLOR yellow]'+pagination.span.text+' >>> [/COLOR]')
            list_item.setArt({'fanart':fanart,'thumb':menu_icon})
            url = get_url(source='KissCartoonSo', endpoint=next_page)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    #http://kisscartoon.so/ (<iframe class="metaframe rptss" src="">)
    iframe_source = soup.find('iframe',{'class':'metaframe rptss'})
    soup = SOUPIFY(iframe_source['src'])
    #http://hnmovies.com/ (<div class="pestana" data-src="">)
    links = []
    titles = []
    dialog = xbmcgui.Dialog()
    link_divs = soup.findAll('div',{'class':'pestana'})
    if len(link_divs) == 0:
        link_divs = soup.findAll('div',{'data-target':'#iframe'})
        links = [div['data-src'] for div in link_divs]
        titles = [div.span.text for div in link_divs]
        ret = dialog.select('Choose a Source', titles)
        if ret > -1:
            link_source = links[ret]
            if not link_source.startswith('http'):
                link_source = SOUPIFY('http:'+link_source)
                try: links.append(link_source.iframe['src'])
                except:
                    removed = re.compile("""This video doesn't exist""").findall(str(link_source))[0]
                    if removed:
                        e = 'This video has been removed. Please try another link'
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, e, 10000, icon))
                        return
                    juicy_code = re.compile("""JuicyCodes.Run\("(.+?)"\)""").findall(str(link_source))[0].replace('"+"','')
                    js = base64.b64decode(juicy_code)
                    jsdone=jsunpack.unpack(js)
                    print jsdone
                    match=re.compile("""file":"([^"']+)","label":"([^"']+)""").findall(jsdone)
                    titles = []
                    for url, quality in match:
                        links.append(url)
                        titles.append(quality)
            else:
                links.append(link_source)
                titles.append('')
    else:
        for i, link in enumerate(link_divs):
            if not link['data-src'].startswith('http'):
                soup = SOUPIFY('http:'+link['data-src'])
                links.append(soup.find('iframe')['src'])
            else:
                links.append(link['data-src'])
            titles.append('Link %s'%str(i+1))
                
    ret = dialog.select('Choose a Stream', titles)
    if ret > -1:
        play_link = links[ret]
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
        soup = SOUPIFY(query+title)
        containers = soup.findAll('div',{'class':'result-item'})
        if len(containers) == 0 and any(x for x in ['&' in title,'%26' in title]):
            new_term = title.replace('&','and').replace('%26','and')
            print '=====re-searching for ({}) on ({})====='.format(new_term,'kisscartoonso')
            soup = SOUPIFY(query+new_term)
            containers = soup.findAll('div',{'class':'result-item'})
        
        titles = [regulate.unescape(div.find('div',{'class':'title'}).a.text+' ('+div.find('div',{'class':'image'}).div.a.span.text+') [COLOR blue]KISSCARTOONSO[/COLOR]') for div in containers]
        images = [div.find('div',{'class':'image'}).div.a.img['src'] for div in containers]
        links = [div.find('div',{'class':'image'}).div.a['href'] for div in containers]
        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    if params:
        link = params.get('endpoint')
        if link.endswith('/top-imdb/'): TOP_IMDB()
        elif link.endswith('/cartoon-movies/'): CARTOON_MOVIES(link)
        elif link.endswith('/cartoon-series/'): CARTOON_SERIES(link)
        elif link.endswith('/episodes/'): CARTOON_SERIES_EPISODES(link)
        elif link.endswith('/seasons/'): CARTOON_SERIES_SEASONS(link)
        
        elif all(x in link for x in ['/cartoon-series/','/page/']): CARTOON_SERIES(link)
        elif all(x in link for x in ['/cartoon-movies/','/page/']): CARTOON_MOVIES(link)
        elif all(x in link for x in ['/seasons/','/page/']): CARTOON_SERIES_SEASONS(link)
        elif all(x in link for x in ['/episodes/','/page/']): CARTOON_SERIES_EPISODES(link)
        
        elif '/seasons/' in link: CARTOON_SERIES_SEASON(link)
        elif '/cartoon-series/' in link: CARTOON_SERIES_EPISODES(link)
        elif any(x in link for x in ['/cartoon-movies/','/episodes/']): PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()

if __name__ == '__main__':
    router(sys.argv[2][1:])