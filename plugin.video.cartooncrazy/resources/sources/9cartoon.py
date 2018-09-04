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
import sys
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
menu_icon = xbmc.translatePath(path+'resources/images/9cartoon_me.png')
addonname = addon.getAddonInfo('name')
with open(xbmc.translatePath(path+'cookies.lwp'), "a") as f: file_var = f 
cookie_file = xbmc.translatePath(path+'cookies.lwp')
base = 'http://9cartoon.me/'
query = base+'Search?s='
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
#useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
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
    url = get_url(source='9Cartoon', endpoint=base+'CartoonList')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Popular')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Cartoon', endpoint=base+'CartoonList/MostViewed')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Latest Update')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Cartoon', endpoint=base+'CartoonList/LatestUpdate')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

    list_item = xbmcgui.ListItem(label='New & Hot')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Cartoon', endpoint=base+'CartoonList/NewAndHot')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='New Added')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Cartoon', endpoint=base+'CartoonList/New')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Cartoon', endpoint=base)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRES(link):
    soup = SOUPIFY(link)
    genres = soup.findAll('li',{'class':['even','oven']})
    titles = [regulate.unescape(li.a.text.strip()) for li in genres if li.a.text.strip() != '']
    links = [li.a['href'] for li in genres if li.a.text.strip() != '']
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='9Cartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRE(link):
    soup = SOUPIFY(link)
    genre = soup.findAll('div',{'class':'last_episodes_items'})
    titles = [regulate.unescape(div.a['title']) for div in genre]
    
    background_img = re.compile("background: url\('(.+?)'\)") 
    images = [background_img.findall(div.a.div['style'])[0]+"|User-Agent="+useragent+"&Cookie=%s"%getCookiesString() for div in genre]
    links = [div.a['href'] for div in genre]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='9Cartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
        
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LATESTUPDATE(link):
    soup = SOUPIFY(link)
    series_lis = soup.find('div',{'class':'anime_list_body'}).findAll('li')
    floating_divs = soup.findAll('div',{'style':'float: left; width: 300px'})
    images = [div.find('div',{'class':'thumnail_tool'}).img['src']+"|User-Agent="+useragent+"&Cookie=%s"%getCookiesString() for div in series_lis]
    [div.extract() for div in floating_divs]
    titles = [regulate.unescape(li.a['title']+' '+li.span.text) for li in series_lis]
    links = [li.a['href'] for li in series_lis]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='9Cartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    series_lis = soup.find('ul',{'class':'listing '}).findAll('li')
    
    floating_divs = soup.findAll('div',{'style':'float: left; width: 300px'})
    images = [div.find('div',{'class':'thumnail_tool'}).img['src']+"|User-Agent="+useragent+"&Cookie=%s"%getCookiesString() for div in series_lis]
    [div.extract() for div in floating_divs]
    
    titles = [regulate.unescape(li.a.text.rstrip().strip()) for li in series_lis]
    links = [li.a['href'] for li in series_lis]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='9Cartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LINKS(link):
    soup = SOUPIFY(link)
    link_lis = soup.find('ul',{'id':'episode_related'}).findAll('li')
    titles = [regulate.unescape(li.a.text) for li in link_lis]
    image = soup.find('div',{'class':'anime_info_body_bg'}).img['src']
    image = image+"|User-Agent=%s&Cookie=%s"%(useragent,getCookiesString())
    links = [li.a['href'] for li in link_lis]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='9Cartoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    pagination = soup.find('ul',{'class':'pages'})
    if pagination is not None:
        next_page_li = pagination.find('li',{'class':'next'})
        if next_page_li is not None:
            try:
                next_page = next_page_li.a['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='9Cartoon', endpoint=base+next_page[1:])
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
            except:
                pass

def PLAY_VIDEO(link):
    referrer = link
    soup = SOUPIFY(link)
    player = soup.find('div',{'id':'player'}).iframe['src']
    soup = SOUPIFY(player)
    try: l = soup.find('iframe')['src']
    except: l = soup.find('source')['src']
    
    if '/rd.php' in l: l = l+"|User-Agent=%s&Cookie=%s"%(useragent,getCookiesString())
    elif any(source in l for source in ['openload.co/embed','googlevideo.com']): pass
    else:
        url = urllib.unquote(l)
        headers = {'Content-Type':'application/x-www-form-urlencoded','Referer': referer}
        link=cleanHex(net.http_GET(url,headers).content)
        js=re.compile('</div></div></div></div><script>(.+?)</script><script>eval').findall(link)[0]
        jsdone=jsunpack.unpack(js)
        url=re.compile('<source src="(.+?)" type="video/mp4"').findall(jsdone)[0]
        l=url+"|User-Agent=%s&Referer=%s&Cookie=%s"%(useragent,url,getCookiesString())
    
    if urlresolver.HostedMediaFile(l).valid_url():
        link = urlresolver.HostedMediaFile(l).resolve()
    else:
        link = l
    li = xbmcgui.ListItem('')
    li.setPath(link)
    xbmc.Player().play(link, li, False)
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
        soup = SOUPIFY(query+title)
        containers = soup.findAll('div',{'class':'last_episodes_items'})
        if len(containers) == 0 and '&' in title:
            soup = SOUPIFY(query+title.replace('&','and'))
            containers = soup.findAll('div',{'class':'last_episodes_items'})
            
        titles = [regulate.unescape(div.a['title']+' [COLOR blue]9CARTOON[/COLOR]') for div in containers]
        background_img = re.compile("background: url\('(.+?)'\)") 
        images = [background_img.findall(div.a.div['style'])[0]+"|User-Agent="+useragent+"&Cookie=%s"%getCookiesString() 
                  for div in containers]
        links = [div.a['href'] for div in containers]
        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if link == base: CARTOON_GENRES(link)
        elif link.startswith(base+'CartoonList/MostViewed'): CARTOON_LIST(link)
        elif link.startswith(base+'CartoonList/LatestUpdate'): CARTOON_LATESTUPDATE(link)
        elif link.startswith(base+'CartoonList/NewAndHot'): CARTOON_LIST(link)
        elif link.startswith(base+'CartoonList/New'): CARTOON_LIST(link)
        elif link.startswith(base+'CartoonList'): CARTOON_LIST(link)
        elif link.startswith(base+'Genre/'): CARTOON_GENRE(link)
        elif link.startswith(base+'Cartoon/'): CARTOON_LINKS(link)
        elif link.startswith(base+'Watch/'): PLAY_VIDEO(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()      
              
if __name__ == '__main__':
    router(sys.argv[2][1:])