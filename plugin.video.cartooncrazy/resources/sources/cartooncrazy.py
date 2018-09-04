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
menu_icon = xbmc.translatePath(path+'resources/images/cartooncrazy_net.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
with open(xbmc.translatePath(path+'cookies.lwp'), "a") as f: file_var = f 
cookie_file = xbmc.translatePath(path+'cookies.lwp')
base = 'http://ww1.cartooncrazy.net/'
query = base+'?s='
movies_php = 'http://ww1.cartooncrazy.net/ep.php?id=1594'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    content = utils.getHtml(link)
    return BeautifulSoup(content)
    
def MAIN_MENU():
    list_item = xbmcgui.ListItem(label='Cartoon List')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonCrazy', endpoint=base+'cartoon-list/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Cartoon Movies [COLOR red]Hit or Miss[/COLOR]')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonCrazy', endpoint=base+'cartoon/cartoon-movies/')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    series = soup.find('div',{'class':'multi-column-taxonomy-list'}).findAll('li')[1:]
    titles = [regulate.unescape(li.a.text).replace('(',' (').replace('  ',' ') for li in series]
    links = [base+li.a['href'][1:] for li in series]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='CartoonCrazy', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SERIES(link):
    soup = SOUPIFY(link)
    php_url = re.compile("""\$\("#load"\).load\('(.+?)'\)""").findall(str(soup))[0]
    soup = SOUPIFY(php_url)

    series = soup.find('table',{'id':'episode-list-entry-tbl'}).findAll('a')
    titles = [regulate.unescape(a.h2.text) for a in series]
    links = [regulate.unescape(base+a['href'][1:]) for a in series]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='CartoonCrazy', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)
    
def CARTOON_MOVIES(link):
    soup = SOUPIFY(link)
    movies = soup.find('table',{'id':'episode-list-entry-tbl'}).findAll('a')
    titles = [regulate.unescape(a.h2.text) for a in movies]
    links = [regulate.unescape(base+a['href'][1:]) for a in movies]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='CartoonCrazy', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    try:
        pagination = soup.findAll('div',{'class':'pagination'})[-1]
        if pagination is not None:
            next_page_a = pagination.findAll('a')[-1]
            if next_page_a is not None:
                if 'Next' in next_page_a.text:
                    try:
                        next_page = next_page_a['href']
                        list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                        url = get_url(source='CartoonCrazy', endpoint=next_page)
                        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
                    except:
                        pass
    except:
        pass

def PLAY_VIDEO(link):
    play_links = []
    titles = []
    soup = SOUPIFY(link)
    l = soup.find('div',{'class':'video_div'}).iframe['src']
    soup = SOUPIFY(l)
    try:
        l = soup.find('iframe')['src']
        req = requests.get(l)
        #print req.content
        l = re.compile("""playerInstance.setup\({\n*\s*file:\s*["']([^"']+)""").findall(req.content)[0]
        play_links.append(l)
        titles.append('Link 1')
    except:
        match=re.compile("""file:\s*["']([^"']+).+?\s*label:\s*["']([^"']+)""").findall(str(soup))
        for url, quality in match:
            play_links.append(url)
            titles.append(quality)
    
    dialog = xbmcgui.Dialog()
    ret = dialog.select('Choose a Stream', titles)
    if ret > -1:
        play_link = play_links[ret]+"|User-Agent="+useragent+"&Cookie=%s"%getCookiesString()
        if urlresolver.HostedMediaFile(play_link).valid_url():
            try:
                play_link = urlresolver.HostedMediaFile(play_link).resolve()
            except:
                play_link = play_link
        li = xbmcgui.ListItem('')
        li.setPath(play_link)
        xbmc.Player().play(play_link, li, False)
        quit()
    
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
    
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
        link = []
        soup = SOUPIFY(query+title)
        containers = soup.find('div',{'id':'main'}).findAll('td')
        if len(containers) == 0 and '&' in title:
            soup = SOUPIFY(query+title.replace('&','and'))
            containers = soup.find('div',{'id':'main'}).findAll('td')
        
        titles = [regulate.unescape(td.text+' [COLOR blue]CARTOONCRAZY[/COLOR]') for td in containers]
        images = [td.a.img['src']+"|User-Agent="+useragent+"&Cookie=%s"%getCookiesString() for td in containers]
        links = [td.a['href'] for td in containers]
        return zip(titles, images, links)
    except:
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if link.startswith(base+'cartoon-list/'): CARTOON_LIST(link)
        elif link.startswith(base+'cartoon/'): CARTOON_SERIES(link)
        elif link.startswith(base+'cartoon/cartoon-movies/'): CARTOON_MOVIES(movies_php)
        elif link.startswith(base+'watch/'): PLAY_VIDEO(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()      
              
if __name__ == '__main__':
    router(sys.argv[2][1:])