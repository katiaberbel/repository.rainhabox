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

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = xbmc.translatePath(path+'resources/images/animetoon.png')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'http://www.animetoon.org'
query = base+'/toon/search?key='
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)

def MAIN_MENU():
    soup = SOUPIFY(base)
    menu_items = soup.find('ul', {'class': 'menu-bar'}).findAll('li')[1:-1]
    categories = [regulate.unescape(menu_item.a.text) for menu_item in menu_items]
    category_links = [menu_item.a['href'] for menu_item in menu_items]
    
    for i, link in enumerate(category_links):
        list_item = xbmcgui.ListItem(label=categories[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Dubbed Anime Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='Animetoon', endpoint=base+'/dubbed-anime-genres')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

#Covers listing genres
def CARTOON_GENRES(link):
    soup = SOUPIFY(link)
    video_genres = soup.find('table').findAll('tr')[2:]
    
    genres = [regulate.unescape(tr.td.a.text+' ('+tr.findAll('td')[-1].text+')') for tr in video_genres]
    links = [tr.td.a['href'] for tr in video_genres]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=genres[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
       
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

#Covers listing series of a genre
def CARTOON_GENRE(link):
    soup = SOUPIFY(link)
    series_containers = soup.find('div',{'class':'series_list'}).findAll('li')
    
    titles = [regulate.unescape(li.find('div',{'class':'right_col'}).h3.a.text) for li in series_containers]
    images = [li.find('div',{'class':'left_col'}).a.img['src'] for li in series_containers]
    links = [li.find('div',{'class':'left_col'}).a['href'] for li in series_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

#Covers listing 'cartoons' main menu item
def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    series_list = soup.findAll('td')

    titles = [regulate.unescape(td.a.text) for td in series_list if td.text != '&nbsp;']
    links = [td.a['href'] for td in series_list if td.text != '&nbsp;']
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

#Covers listing 'popular' main menu item
def CARTOON_POPULAR(link):
    soup = SOUPIFY(link)
    series_containers = soup.findAll('div',{'class':'series_list'})[1].findAll('li')
    
    titles = [regulate.unescape(li.find('div',{'class':'right_col'}).h3.a.text) for li in series_containers]
    images = [li.find('div',{'class':'left_col'}).a.img['src'] for li in series_containers]
    links = [li.find('div',{'class':'left_col'}).a['href'] for li in series_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

#Covers listing 'updates' main menu item
def CARTOON_LATEST(link):
    soup = SOUPIFY(link)
    update_containers = soup.findAll('tr')
    
    titles = [regulate.unescape(tr.td.ul.li.a.text+' ('+tr.findAll('td')[-1].text.strip().rstrip()+')')
              for tr in update_containers]
    links = [tr.td.ul.li.a['href'] for tr in update_containers]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)    

#Covers listing episodes of a show
def CARTOON_SERIES(link):
    soup = SOUPIFY(link)
    try:
        #This is collecting all available episodes of a show
        series_container = soup.find('div',{'id':'videos'}).findAll('li')
        image = soup.find('img',{'id':'series_image'})['src']
        titles = [regulate.unescape(li.a.text) for li in series_container]
        links = [li.a['href'] for li in series_container]
    except:
        #This is collecting all available links for the episode/movie
        image = menu_icon
        series_container = soup.findAll('div',{'class':'vmargin'})
        part_list = soup.findAll('ul',{'class':'part_list'})
        """
        if len(part_list)>0:
            titles = [div.div.span.text+' ' for div in series_container]
            for s, source in enumerate(series_container):
                for p, part in enumerate(part_list[s]):
                    part_list[s]= titles[s]+part.text
            titles = part_list
            links = [div.find('iframe')['src'] for div in series_container]
            print list(titles)
        else:
        """
        
        titles = [regulate.unescape(div.div.span.text) for div in series_container]
        links = [div.find('iframe')['src'] for div in series_container]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        if image is not None: list_item.setArt({'fanart':fanart,'thumb':image})
        else: list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='Animetoon', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def GET_NEXT_PAGE(soup):
    pagination = soup.find('ul',{'class':'pagination'})
    if pagination is not None:
        next_page_li = pagination.findAll('li')[-1]
        if next_page_li is not None:
            try:
                next_page = next_page_li.a['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='Animetoon', endpoint=next_page_li.a['href'])
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
            except:
                pass

def PLAY_VIDEO(link):
    print link
    source_html = requests.get(link)
    c = source_html.content
    if c.find('_url = "') > 0:
        l = c[c.find('_url = "')+8:c.find('"',c.find('_url = "')+9)]
        l = urllib.unquote(l).decode('utf8')
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

    print play_link
    li = xbmcgui.ListItem('')
    li.setPath(play_link)
    xbmc.Player().play(play_link, li, False)

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query+title)
        series_containers = soup.find('div',{'class':'series_list'}).findAll('li')
        if len(series_containers) == 0 and any(x for x in ['&' in title,'%26' in title]):
            new_term = title.replace('&','and').replace('%26','and')
            print '=====re-searching for ({}) on ({})====='.format(new_term,'animetoon')
            soup = SOUPIFY(query+new_term)
            series_containers = soup.find('div',{'class':'series_list'}).findAll('li')
        
        titles = [regulate.unescape(li.find('div',{'class':'right_col'}).h3.a.text+' [COLOR blue]ANIMETOON[/COLOR]') for li in series_containers]
        images = [li.find('div',{'class':'left_col'}).a.img['src'] for li in series_containers]
        links = [li.find('div',{'class':'left_col'}).a['href'] for li in series_containers]
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
        if link.endswith('-genres'): CARTOON_GENRES(link)
        elif '-genre/' in link: CARTOON_GENRE(link)
        elif link.endswith('/cartoon'): CARTOON_LIST(link)
        elif link.endswith('/dubbed-anime'): CARTOON_LIST(link)
        elif link.endswith('/movies'): CARTOON_LIST(link)
        elif link.endswith('/updates'): CARTOON_LATEST(link)
        elif '/updates/' in link: CARTOON_LATEST(link)
        elif link.endswith('/popular-list'): CARTOON_POPULAR(link)
        elif '/popular-list/' in link: CARTOON_POPULAR(link)
        elif link.startswith(base): CARTOON_SERIES(link)
        elif link is not None: PLAY_VIDEO(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()

if __name__ == '__main__':
    router(sys.argv[2][1:])