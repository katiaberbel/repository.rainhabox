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
menu_icon = xbmc.translatePath(path+'resources/images/cartoonson_com.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://www.cartoonson.com/'
query = base+'search/search/q/%s'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)

def MAIN_MENU():
    soup = SOUPIFY(base)

    list_item = xbmcgui.ListItem(label='By Studio')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonsOn', endpoint=base+'cartoons/all-studios')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='By Character')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonsOn', endpoint=base+'cartoons/all-characters')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='By Series')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonsOn', endpoint=base+'cartoons/all-series')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='By Cartoon')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonsOn', endpoint=base)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Latest Updates')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonsOn', endpoint=base, part='Latest Updates')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Most Watched')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='CartoonsOn', endpoint=base, part='Most Watched')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LATEST(link):
    soup = SOUPIFY(link)
    latest_updates = soup.findAll('div',{'class':'item'})
    titles = [regulate.unescape(div.small.a.text+' '+div.findAll('small')[-1].a.text+' '+div.h4.a.text)
              for div in latest_updates]
    images = [div.a.img['src'] for div in latest_updates]
    links = [div.a['href'] for div in latest_updates]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='CartoonsOn', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)
    
def CARTOON_MOST_WATCHED(link):
    soup = SOUPIFY(link)
    most_watched = soup.find('section',{'id':'under_content'}).find('p').findAll('a')
    titles = [regulate.unescape(a.text.replace('&nbsp;',' ')) for a in most_watched]
    links = [base+a['href'][1:] for a in most_watched]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='CartoonsOn', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    show_containers = soup.findAll('li',{'class':'media col-sm-4'})
    if len(show_containers) == 0: PLAY_VIDEO(link.replace('/view/','/watch/'))
    
    titles = [regulate.unescape(li.div.img['alt']) for li in show_containers]
    images = [li.div.img['src'] for li in show_containers]
    links = [li.div.div.a['href'] for li in show_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='CartoonsOn', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SEASONS(link):
    soup = SOUPIFY(link)
    season_containers = soup.findAll('div',{'class':'col-sm-3'})
    #if len(season_containers) == 0: CARTOON_LIST(link)
    if len(season_containers) == 0: CARTOON_EPISODES(link)
    
    titles = [regulate.unescape(div.a.img['alt']) for div in season_containers]
    images = [div.a.img['data-src'] for div in season_containers]
    links = [div.a['href'] for div in season_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='CartoonsOn', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_EPISODES(link):
    soup = SOUPIFY(link)
    episode_containers = soup.find('div',{'class':'panel-group'})
    if len(episode_containers) == 0: CARTOON_LIST(link)
    
    image = soup.find('img',{'class':'img-responsive'})['src']
    titles = [regulate.unescape(div.find('div',{'class':'panel-body'}).p.text) for div in episode_containers]
    links = [div.find('a',{'class':'pull-right play-episode-btn btn btn-default'})['href'] for div in episode_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':image})
        url = get_url(source='CartoonsOn', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    pagination = soup.find('ul',{'class':'pagination'})
    if pagination is not None:
        current_page = int(pagination.find('li',{'class':'active'}).text)
        last_page_li = pagination.findAll('li')[-1]
        if last_page_li.a.text == '&raquo;':
            try:
                next_page = last_page_li.a['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='CartoonsOn', endpoint=next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
            except:
                pass

                
def PLAY_VIDEO(link):
    soup = SOUPIFY(link)
    try: link = soup.find('iframe')['src']
    except: link = soup.find('source')['src']
    title = soup.find('div',{'class':'page_title_section'}).h1.text.split(',')[-1]
    if urlresolver.HostedMediaFile(link).valid_url():
        try: play_link = urlresolver.HostedMediaFile(link).resolve()
        except: link = link
    else: 
        link = link
    li = xbmcgui.ListItem(title)
    li.setPath(link)
    xbmc.Player().play(link, li, False)
    quit()

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query % title)
        containers = soup.findAll('div',{'class':'search-item'})
        if len(containers) == 0 and '&' in title:
            soup = SOUPIFY(query % title.replace('&','and'))
            containers = soup.findAll('div',{'class':'search-item'})
        
        titles = [regulate.unescape(div.h3.a.text+' [COLOR blue]CARTOONSON[/COLOR]') for div in containers]
        images = ['' for div in containers]
        links = [base+div.h3.a['href'][1:] for div in containers]
        return zip(titles, images, links)
    except:
        link = []
        return links

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    if params:
        link = params.get('endpoint')
        print link
        part = params.get('part')
        if link == base and part == 'Latest Updates': CARTOON_LATEST(base)
        elif link == base and part == 'Most Watched': CARTOON_MOST_WATCHED(base)
        elif link == base: CARTOON_LIST(base)
        elif link.startswith(base+'cartoons&pg='): CARTOON_LIST(link)
        elif link.startswith(base+'cartoons/watch-preview/'): PLAY_VIDEO(link.replace('-preview/','/'))
        elif link.startswith(base+'cartoons/all-studios'): CARTOON_LIST(link)
        elif link.startswith(base+'cartoons/list/studio/'): CARTOON_LIST(link)
        elif link.startswith(base+'cartoons/all-characters'): CARTOON_LIST(link)
        elif link.startswith(base+'cartoons/list/character/'): CARTOON_LIST(link)
        elif link.startswith(base+'cartoons/all-series'): CARTOON_LIST(link)
        elif link.startswith(base+'cartoons/list/serie/'): CARTOON_SEASONS(link)
        elif '/season/' in link: CARTOON_EPISODES(link)
        elif 'cartoons/view/id/' in link: CARTOON_SEASONS(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()

if __name__ == '__main__':
    router(sys.argv[2][1:])